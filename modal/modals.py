import os
import pickle

from sympy import diff
from sympy import symbols
from sympy import integrate
from modal.operating_mode import get_operation_mode, get_operation_mode_map

# 获取不同工况
conditions = get_operation_mode_map()
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_distance(condition):
    distance = 0
    for i in range(len(condition) - 1):
        [cur_time, cur_velocity] = condition[i]
        [next_time, next_velocity] = condition[i + 1]
        distance += (cur_velocity + next_velocity) * (next_time - cur_time) / 2
    return distance


highway_type_name = dict(
    residential='住宅',
    primary='主要',
    tertiary='第三',
    secondary='次要',
    trunk='主干',
    motorway='高速公路',
    motorway_link='高速公路',
    primary_link='主要',
    unclassified='未分类',
    secondary_link='次要',
    trunk_link='干线',
    living_street='生活',
    tertiary_link='第三'
)


class WeightFn:
    def __init__(self, weight_fn):
        self.consumptions = []

        def fn_with_consumption(*args):
            consumption = weight_fn(*args)
            self.consumptions.append(consumption)
            return consumption

        self.fn = weight_fn
        self.fn_with_consumption = fn_with_consumption

    def get_consumptions(self):
        return self.consumptions

    def clear_consumptions(self):
        self.consumptions.clear()


class Modal:
    def __init__(self, name):
        print(f'开始创建{name}实例')
        self.name = name  # 名字
        self.g = 9.8  # 重力加速度 g/（m/s2）
        self.weight_fn = {}

    # 从本地读取计算好的结果
    def get_average_from_local(self, weight_name):
        with open(f'{dir_path}/data/{self.name}_{weight_name}', 'rb') as f:
            return pickle.load(f)

    # 获取需要的权重函数
    def get_weight_fn(self, weight_fn_type) -> WeightFn:
        return self.weight_fn[weight_fn_type]

    # 计算所所有平均消耗并进行本地化
    def localization(self):
        return


# 有制动回收的电动车
class ElectricVehicle(Modal):
    def __init__(self, m, delta, eta_T, eta_m, eta_b, eta_c, C_D, A, f, k, name=None):
        super().__init__(name)
        self.m = m  # 整备质量 m/kg
        self.delta = delta  # 汽车旋转质量换算系数 δ
        self.eta_T = eta_T  # 机械传动效率ηT
        self.eta_m = eta_m  # 电机工作效率ηm
        self.eta_b = eta_b  # 电池效率ηb
        self.eta_c = eta_c  # 制动回收效率ηc
        self.C_D = C_D  # 空气阻力系数 CD
        self.A = A  # 迎风面积 A/m2
        self.f = f  # 滚动阻力系数 f
        self.k = k  # 电气制动比例
        print('开始构造最小能耗权重计算函数')
        energy = self.__private_create_consumption_weight_fn()
        print('最小能耗权重计算函数构造完成')
        print('开始构造最小耗时权重计算函数')
        velocity = self.__private_create_velocity_weight_fn()
        print('最小耗时权重计算函数构造完成')
        self.weight_fn = {
            'energy': energy,
            'velocity': velocity
        }

    # 获取不同工况的平均耗能（kj/m）
    def get_average_consumption(self):
        def E_1(v1, v2, t1, t2):
            t = symbols("t")  # 需要进行求导的变量t
            a = (v2 - v1) / (t2 - t1)
            v0 = v1 - a * t1
            v = v0 + a * t  # 汽车行驶速度v(t)

            return integrate(1 / (self.eta_T * self.eta_m * self.eta_b) * (
                    (self.m * self.g * self.f * v) / 3600 + (self.C_D * self.A * v ** 3) / 76140 + diff(
                (self.delta * self.m * v) / 3600, t)), (t, t1, t2))

        # 匀速阶段
        def E_2(v, t):
            return t / (self.eta_T * self.eta_m * self.eta_b) * (
                    (self.m * self.g * self.f * v) / 3600 + (self.C_D * self.A * v ** 3) / 76140)

        # 制动阶段
        def E_3(v1, v2, t1, t2):
            t = symbols("t")  # 需要进行求导的变量t
            a = (v2 - v1) / (t2 - t1)
            v0 = v1 - a * t1
            v = v0 + a * t  # 汽车行驶速度v(t)
            return (1 / 3.6) ** 3 * ((1 - self.eta_c) / (10 ** 6 * self.eta_T * self.eta_m * self.eta_b)) * (
                    (1 / 2 * self.m * v2 ** 2) - (1 / 2 * self.m * v1 ** 2)) - (
                    self.k * self.eta_c * integrate(
                (self.m * self.g * self.f * v) / 3600 + (self.C_D * self.A * v ** 3) / 76140 + diff(
                    (self.delta * self.m * v) / 3600, t),
                (t, t1, t2)
            ) / (self.eta_T * self.eta_m * self.eta_b)
            )
        res = {}
        for key, condition in conditions.items():
            consume = 0
            distance = get_distance(condition)
            for i in range(len(condition) - 1):
                [cur_time, cur_velocity] = condition[i]
                [next_time, next_velocity] = condition[i + 1]
                if cur_velocity == next_velocity:
                    consume += E_2(cur_velocity, next_time - cur_time)
                elif cur_velocity >= next_velocity:
                    consume += E_3(cur_velocity, next_velocity, cur_time, next_time)
                else:
                    consume += E_1(cur_velocity, next_velocity, cur_time, next_time)
            res[key] = consume / distance * 1.05
        return res

    # 构造规划最小能耗所需的权重计算函数
    def __private_create_consumption_weight_fn(self):
        # 计算各种工况下的平均能耗（kW·h/km）
        average_consumption = self.get_average_from_local('energy')
        print(average_consumption)

        # 权重计算函数
        def weight_fn(start_node_id, end_node_id, edge):
            # 传入边和节点信息，用于计算路段的能耗
            highway_type = edge[0]['highway']
            highway_length = edge[0]['length']
            # 根据传入的参数分辨所属的工况
            operation_mode = get_operation_mode(highway_type)
            # 计算路段的能耗
            consumption = average_consumption[operation_mode] * highway_length
            return consumption

        return WeightFn(weight_fn)

    # 获取不同工况的平均耗时（m/s）
    @staticmethod
    def get_average_velocity():
        res = {}
        for key, condition in conditions.items():
            distance = get_distance(condition)
            res[key] = distance / 500
        return res

    # 构造规划最快速度所需的权重计算函数
    def __private_create_velocity_weight_fn(self):
        # 计算各种工况下的平均速度（kW·h/km）
        average_velocity = self.get_average_from_local('velocity')
        average_velocity['congestion'] += 5
        average_velocity['normal'] -= 3
        average_velocity['unobstructed'] -= 15
        print(average_velocity)

        def weight_fn(start_node_id, end_node_id, edge):
            highway_type = edge[0]['highway']
            highway_length = edge[0]['length']
            # 根据传入的参数分辨所属的工况
            operation_mode = get_operation_mode(highway_type)

            return highway_length / average_velocity[operation_mode]

        return WeightFn(weight_fn)

    # 计算所所有平均消耗并进行本地化
    def localization(self):
        print('开始构造最小能耗权重计算函数')
        energy = self.get_average_consumption()
        print('最小能耗权重计算函数构造完成')
        print('开始构造最小耗时权重计算函数')
        velocity = self.get_average_velocity()
        print('最小耗时权重计算函数构造完成')
        with open(f'{dir_path}/data/{self.name}_energy', 'wb') as f:
            pickle.dump(energy, f)
        with open(f'{dir_path}/data/{self.name}_velocity', 'wb') as f:
            pickle.dump(velocity, f)
        return


# 传统燃油车
class TraditionalVehicle(Modal):
    def __init__(self, name, m, delta, eta_T, C_D, A, f, k):
        super().__init__(name)
        self.m = m  # 整备质量 m/kg
        self.delta = delta  # 汽车旋转质量换算系数 δ
        self.eta_T = eta_T  # 机械传动效率ηT
        self.C_D = C_D  # 空气阻力系数 CD
        self.A = A  # 迎风面积 A/m2
        self.f = f  # 滚动阻力系数 f
        self.k = k  # 电气制动比例
        print('开始构造最小能耗权重计算函数')
        energy = self.__private_create_consumption_weight_fn()
        print('最小能耗权重计算函数构造完成')
        print('开始构造最小耗时权重计算函数')
        velocity = self.__private_create_velocity_weight_fn()
        print('最小耗时权重计算函数构造完成')
        self.weight_fn = {
            'energy': energy,
            'velocity': velocity
        }

    # 获取不同工况的平均耗能（kj/m）
    def get_average_consumption(self):
        def E(v1, v2, t1, t2):
            t = symbols("t")  # 需要进行求导的变量t
            a = (v2 - v1) / (t2 - t1)
            v0 = v1 - a * t1
            v = v0 + a * t  # 汽车行驶速度v(t)

            return integrate((self.m * self.g * self.f * v) / 3600 + (self.C_D * self.A * v ** 3) / 76140 + (
                    self.delta * self.m * v) * diff(v, t) / 3600, (t, t1, t2)) / self.eta_T
        res = {}
        for key, condition in conditions.items():
            consume = 0
            distance = get_distance(condition)
            for i in range(len(condition) - 1):
                [cur_time, cur_velocity] = condition[i]
                [next_time, next_velocity] = condition[i + 1]
                consume += E(cur_velocity, next_velocity, cur_time, next_time)
            res[key] = consume / distance * 3
        return res

    # 构造规划最小能耗所需的权重计算函数
    def __private_create_consumption_weight_fn(self):
        average_consumption = self.get_average_from_local('energy')
        average_consumption['congestion'] += 0.5
        average_consumption['unobstructed'] -= 0.2
        print(average_consumption)

        def weight_fn(start_node_id, end_node_id, edge):
            highway_type = edge[0]['highway']
            highway_length = edge[0]['length']
            operation_mode = get_operation_mode(highway_type)
            return average_consumption[operation_mode] * highway_length

        return WeightFn(weight_fn)

    # 获取不同工况的平均耗时（m/s）
    @staticmethod
    def get_average_velocity():
        res = {}
        for key, condition in conditions.items():
            distance = get_distance(condition)
            res[key] = distance / 500
        return res

    # 构造规划最快速度所需的权重计算函数
    def __private_create_velocity_weight_fn(self):
        average_velocity = self.get_average_from_local('velocity')
        average_velocity['congestion'] += 5
        average_velocity['normal'] -= 3
        average_velocity['unobstructed'] -= 15
        print(average_velocity)

        def weight_fn(start_node_id, end_node_id, edge):
            highway_type = edge[0]['highway']
            highway_length = edge[0]['length']
            operation_mode = get_operation_mode(highway_type)
            return highway_length / average_velocity[operation_mode]

        return WeightFn(weight_fn)

    # 计算所所有平均消耗并进行本地化
    def localization(self):
        print('开始构造最小能耗权重计算函数')
        energy = self.get_average_consumption()
        print('最小能耗权重计算函数构造完成')
        print('开始构造最小耗时权重计算函数')
        velocity = self.get_average_velocity()
        print('最小耗时权重计算函数构造完成')
        with open(f'{dir_path}/data/{self.name}_energy', 'wb') as f:
            pickle.dump(energy, f)
        with open(f'{dir_path}/data/{self.name}_velocity', 'wb') as f:
            pickle.dump(velocity, f)
        return
