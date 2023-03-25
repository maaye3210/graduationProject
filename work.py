import osmnx as ox

print('start')
file_path = './demtest/huancui_with_dem.graphml'
G = ox.load_graphml(file_path)  # 第一步，获取道路数据
origin_point = (37.53184, 122.07468)  # 七公寓坐标
destination_point = (37.50542, 122.11810)  # 威高坐标
origin_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])  # 获取O最邻近的道路节点
destination_node = ox.nearest_nodes(G, destination_point[1], destination_point[0])  # 获取D最邻近的道路节点
print('起点节点：', origin_node)
print('目的地节点：', destination_node)

print('遍历边......')
edges = G.edges()
highway_values = []
res = []
for (startNodeId, endNodeId) in edges:
    route_dict = G[startNodeId][endNodeId]
    for index in route_dict:
        if 'highway' in route_dict[index]:
            highway_value = route_dict[index]['highway']
            if highway_value not in highway_values:
                highway_values.append(highway_value)
        else:
            res.append(route_dict[index])

print(highway_values, res)

