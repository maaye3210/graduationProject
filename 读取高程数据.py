import osmnx as ox

file_path = './demtest/huancuihigh.graphml'
G = ox.load_graphml(file_path)  # 第一步，获取道路数据

ox.plot_graph(G)
