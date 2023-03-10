import osmnx as ox
# 地点
place_name = 'huancui, weihai, shandong, China'
names = []
for name in place_name.split(','):
    names.insert(0, name.strip())
save_path = './graph/' + '/'.join(names)

print('开始下载')
graph = ox.graph_from_place(place_name, network_type='drive', clean_periphery=False)
# 存储路网graphml是osmnx中本地化图存储结构
print('开始储存graphml')
ox.save_graphml(graph, save_path + '.graphml')
# 以shp文件保存，可以在Qgis中可视化查看
print('开始储存shapefile')
ox.io.save_graph_shapefile(graph, filepath=save_path, encoding='utf-8', directed=False)
print('储存完成')

print('开始测试数据')
G = ox.load_graphml(save_path + '.graphml')
ox.plot_graph(G)
