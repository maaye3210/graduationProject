import osmnx as ox
import networkx as nx
from flask import Flask
from flask import request

print(__name__)
app = Flask(__name__)
file_path = './graph/China/shandong/weihai/huancui.graphml'
G = ox.load_graphml(file_path)  # 第一步，获取道路数据


def get_success_response(res):
    return {
        'success': True,
        "code": 200,
        "data": res,
    }


def shortest_route(lng1, lat1, lng2, lat2):
    origin_point = (lng1, lat1)  # 起点坐标
    destination_point = (lng2, lat2)  # 终点坐标
    origin_node = ox.nearest_nodes(G, lng1, lat1)  # 获取O最邻近的道路节点
    destination_node = ox.nearest_nodes(G, lng2, lat2)  # 获取D最邻近的道路节点
    print('起点节点：', origin_node, '，目的地节点：', destination_node)

    # 计算路径
    route = nx.shortest_path(G, origin_node, destination_node, weight='length')  # 请求获取最短路径
    distance = nx.shortest_path_length(G, origin_node, destination_node, weight='length')  # 并获取路径长度
    print('距离：' + str(distance))  # 输出最短路径距离
    return {
        'node': (origin_node, destination_node),
        'point': (origin_point, destination_point),
        'route': route,
        'distance': distance
    }


@app.route('/')
def hello_world():
    return '<h1>欢迎使用</h1>'


@app.route('/route')
def get_route():
    lat1 = request.args.get('lat1', default=37.53184, type=float)
    lng1 = request.args.get('lng1', default=122.07468, type=float)
    lat2 = request.args.get('lat2', default=37.50542, type=float)
    lng2 = request.args.get('lng2', default=122.11810, type=float)
    route = shortest_route(lng1, lat1, lng2, lat2)
    return get_success_response(route)


app.run(debug=True)
