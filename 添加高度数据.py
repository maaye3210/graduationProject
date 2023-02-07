import osmnx as ox

path1 = './dem/ASTGTMV003_N37E122_dem.tif'
path2 = './dem/ASTGTMV003_N37E121_dem.tif'
path3 = './dem/ASTGTMV003_N36E121_dem.tif'
path4 = './dem/ASTGTMV003_N36E122_dem.tif'

save_path = './demtest/'

G = ox.load_graphml(save_path + 'huancui.graphml')

print('开始添加高度数据')

ox.add_node_elevations_raster(G, [path1, path2], cpus=1)

print('添加完成')
ox.save_graphml(G, save_path + 'huancui_with_dem.graphml')
print('储存完成')