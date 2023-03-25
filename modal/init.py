import osmnx as ox
import networkx as nx
from modal.operating_mode import get_operation_mode_map
from modal.modals import TraditionalVehicle, ElectricVehicle, Modal

print('start')
file_path = './demtest/huancui_with_dem.graphml'

# 获取道路数据
G = ox.load_graphml(file_path)

# 获取不同工况
conditions = get_operation_mode_map()

# 预设模型
# 传统汽车模型
traditional_modal = TraditionalVehicle(
    name='traditional',
    m=12400,  # 整备质量 m/kg
    eta_T=0.9,  # 机械传动效率ηT
    delta=1.02,  # 汽车旋转质量换算系数 δ
    C_D=0.67,  # 空气阻力系数 CD
    A=2.6,  # 迎风面积 A/m2
    f=0.02,  # 滚动阻力系数 f
    k=0.2  # 电气制动比例
)

# 电动汽车模型
electric_modal = ElectricVehicle(
    name='electric',
    m=12400,  # 整备质量 m/kg
    eta_T=0.9,  # 机械传动效率ηT
    eta_m=0.8,  # 电机工作效率ηm
    eta_b=0.8,  # 电池效率ηb
    delta=1.02,  # 汽车旋转质量换算系数 δ
    eta_c=0.8,  # 制动回收效率ηc
    C_D=0.67,  # 空气阻力系数 CD
    A=2.6,  # 迎风面积 A/m2
    f=0.02,  # 滚动阻力系数 f
    k=0.2  # 电气制动比例
)

# 默认模型，只能计算最短路径
default_modal = Modal('default')

modal_list = [traditional_modal, electric_modal]


class PathPlanner:
    def __init__(self):
        self.modal_list = modal_list

    def get_modal_by_name(self, name) -> Modal:
        for modal in self.modal_list:
            if modal.name == name:
                return modal
        return default_modal

    def get_route(self, origin_point, destination_point, modal_name, weight_type):
        modal = self.get_modal_by_name(modal_name)
        # 构造权重计算函数
        if weight_type == 'length':
            weight_fn = weight_type
        else:
            weight_fn = modal.get_weight_fn(weight_type)
        origin_node = ox.nearest_nodes(G, origin_point[0], origin_point[1])  # 获取O最邻近的道路节点
        destination_node = ox.nearest_nodes(G, destination_point[0], destination_point[1])  # 获取D最邻近的道路节点
        # 计算路径
        route = nx.shortest_path(G, origin_node, destination_node, weight=weight_fn)  # 请求获取最小能耗路径
        cost = nx.shortest_path_length(G, origin_node, destination_node, weight=weight_fn)  # 并获取最小能耗
        path = []
        for index in range(len(route) - 1):
            node = G.nodes[route[index]]
            path.append([node['x'], node['y']])
        return {
            'modal_name': modal_name,
            'weight_type': weight_type,
            'route': route,
            'cost': float(cost),
            'path': path
        }

    @staticmethod
    def get_distance_route(origin_node, destination_node):
        route = nx.shortest_path(G, origin_node, destination_node, weight='length')  # 请求获取最短路径
        distance = nx.shortest_path_length(G, origin_node, destination_node, weight='length')  # 并获取路径长度
        return {
            'route': route,
            'distance': distance
        }
