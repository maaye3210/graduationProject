import osmnx as ox
import networkx as nx
from modal.operating_mode import get_operation_mode_map
from modal.modals import TraditionalVehicle, ElectricVehicle


def get_energy_route(origin_node, destination_node, modal):
    # 构造权重计算函数
    weight_fn = modal.create_consumption_weight_fn(G, conditions)

    # 计算路径
    route = nx.shortest_path(G, origin_node, destination_node, weight=weight_fn)  # 请求获取最小能耗路径
    energy = nx.shortest_path_length(G, origin_node, destination_node, weight=weight_fn)  # 并获取最小能耗

    return {
        'route': route,
        'energy': energy
    }


def get_velocity_route(origin_node, destination_node, modal):
    # 构造权重计算函数
    weight_fn = modal.create_velocity_weight_fn(G, conditions)

    # 计算路径
    route = nx.shortest_path(G, origin_node, destination_node, weight=weight_fn)  # 请求获取最小耗时
    time = nx.shortest_path_length(G, origin_node, destination_node, weight=weight_fn)  # 并获取最小耗时

    return {
        'route': route,
        'time': time
    }


print('start')
file_path = './demtest/huancui_with_dem.graphml'
G = ox.load_graphml(file_path)  # 第一步，获取道路数据
origin_point = (37.53184, 122.07468)  # 七公寓坐标
destination_point = (37.50542, 122.11810)  # 威高坐标
origin_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])  # 获取O最邻近的道路节点
destination_node = ox.nearest_nodes(G, destination_point[1], destination_point[0])  # 获取D最邻近的道路节点
print('起点节点：', origin_node)
print('目的地节点：', destination_node)

conditions = get_operation_mode_map()
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

get_velocity_route(origin_node, destination_node, traditional_modal)
get_velocity_route(origin_node, destination_node, electric_modal)
get_energy_route(origin_node, destination_node, traditional_modal)
get_energy_route(origin_node, destination_node, electric_modal)
