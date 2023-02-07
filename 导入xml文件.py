import osmnx as ox
import networkx as nx

print('start')
G = ox.graph_from_xml('./data/环翠区路线')
ox.plot_graph(G)
origin_point = (37.53184, 122.07468)  # 七公寓坐标
destination_point = (37.48598, 122.1381)  # 研究院坐标
origin_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])  # 获取O最邻近的道路节点
destination_node = ox.nearest_nodes(G, destination_point[1], destination_point[0])  # 获取D最邻近的道路节点
route = nx.shortest_path(G, origin_node, destination_node, weight='length')  # 请求获取最短路径
distance = nx.shortest_path_length(G, origin_node, destination_node, weight='length')  # 并获取路径长度

fig, ax = ox.plot_graph_route(G, route)  # 可视化结果