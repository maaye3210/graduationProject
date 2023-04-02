from flask import Flask
from flask import request
from modal.init import PathPlanner


app = Flask(__name__)

path_planner = PathPlanner()


def get_success_response(res):
    return {
        'success': True,
        "code": 200,
        "data": res,
    }


def get_weight_route(origin_point, destination_point, model_name, weight_type):
    return path_planner.get_route(origin_point, destination_point, model_name, weight_type)


@app.route('/')
def hello_world():
    return '<h1>欢迎使用</h1>'


@app.route('/route')
def short_route():
    lat1 = request.args.get('lat1', default=37.53184, type=float)
    lng1 = request.args.get('lng1', default=122.07468, type=float)
    lat2 = request.args.get('lat2', default=37.50542, type=float)
    lng2 = request.args.get('lng2', default=122.11810, type=float)
    origin_point = (lng1, lat1)  # 起点坐标
    destination_point = (lng2, lat2)  # 终点坐标
    return get_success_response(get_weight_route(origin_point, destination_point, 'default', 'length'))


@app.route('/weightRoute')
def weight_route():
    lat1 = request.args.get('lat1', default=37.53184, type=float)
    lng1 = request.args.get('lng1', default=122.07468, type=float)
    lat2 = request.args.get('lat2', default=37.50542, type=float)
    lng2 = request.args.get('lng2', default=122.11810, type=float)
    model_name = request.args.get('modal_name', default='electric')
    weight_type = request.args.get('weight_type', default='energy')
    origin_point = (lng1, lat1)  # 起点坐标
    destination_point = (lng2, lat2)  # 终点坐标
    res = get_weight_route(origin_point, destination_point, model_name, weight_type)
    print(get_success_response(res))
    return get_success_response(res)


@app.route('/path')
def route_path():
    return []


app.run(debug=True)
