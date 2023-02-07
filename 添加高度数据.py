import osmnx as ox

path1 = './dem/ASTGTMV003_N37E122_dem.tif'
path2 = './dem/ASTGTMV003_N37E121_dem.tif'

# place_name = 'huancui, weihai, shandong, China'

save_path = './demtest/'
#
# print('开始下载')
# graph = ox.graph_from_place(place_name, network_type='drive', clean_periphery=False)
# # 存储路网
# print('开始储存graphml')
# ox.save_graphml(graph, save_path + 'huancui.graphml')
# print('储存完成')
#
# print('开始测试数据')
G = ox.load_graphml(save_path + 'huancui.graphml')
# ox.plot_graph(G)
print('开始添加高度数据')

ox.add_node_elevations_raster(G, [path1, path2], cpus=1)

print('添加完成')
ox.save_graphml(G, save_path + 'huancuihigh.graphml')
print('储存完成')