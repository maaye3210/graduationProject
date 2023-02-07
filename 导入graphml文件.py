import osmnx as ox
import networkx as nx
from utils.getbox import get_box

print('start')
file_path = './graph/China/shandong/weihai/huancui.graphml'
G = ox.load_graphml(file_path)  # 第一步，获取道路数据
origin_point = (37.53184, 122.07468)  # 七公寓坐标
destination_point = (37.50542, 122.11810)  # 威高坐标
origin_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])  # 获取O最邻近的道路节点
destination_node = ox.nearest_nodes(G, destination_point[1], destination_point[0])  # 获取D最邻近的道路节点
print('起点节点：', origin_node)
print('目的地节点：', destination_node)

# 计算路径
route = nx.shortest_path(G, origin_node, destination_node, weight='length')  # 请求获取最短路径
distance = nx.shortest_path_length(G, origin_node, destination_node, weight='length')  # 并获取路径长度

fig, ax = ox.plot_graph_route(G, route, bbox=get_box(origin_point, destination_point))  # 可视化结果
print('距离：' + str(distance))  # 输出最短路径距离
