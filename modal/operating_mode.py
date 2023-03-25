from enum import Enum


# # 所有的行驶工况
# OperationMode = Enum([
#     'congestion',
#     'normal',
#     'unobstructed'
# ])
# # 道路类型
# HighwayType = Enum([
#     'residential', 'primary', 'tertiary', 'secondary', 'trunk', 'motorway', 'motorway_link', 'primary_link',
#     'unclassified', 'secondary_link', 'trunk_link', 'living_street', 'tertiary_link'
# ])
class HighwayTypeEnum(Enum):
    residential = '住宅',
    primary = '主要',
    tertiary = '第三',
    secondary = '次要',
    trunk = '主干',
    motorway = '高速公路',
    motorway_link = '高速公路',
    primary_link = '主要',
    unclassified = '未分类',
    secondary_link = '次要',
    trunk_link = '干线',
    living_street = '生活',
    tertiary_link = '第三'


# 模拟不同状态下的速度时间曲线（行驶工况）
operation_mode_map = {
    'congestion': [
        [5, 0],
        [13, 0.5],
        [16, 2],
        [20, 1.5],
        [40, 3.5],
        [50, 4.5],
        [65, 1],
        [70, 1.4],
        [73, 2.7],
        [80, 0],
        [118, 0],
        [127, 2],
        [132, 1],
        [135, 2],
        [160, 0],
        [260, 0],
        [268, 4],
        [273, 4.5],
        [280, 0],
        [306, 0],
        [312, 1],
        [316, 4],
        [335, 0],
        [400, 0],
        [408, 4],
        [412, 4],
        [417, 2],
        [445, 4],
        [460, 14],
        [465, 12],
        [476, 10],
        [486, 0]
    ],
    'normal': [
        [0, 0],
        [10, 0],
        [16, 20],
        [33, 5],
        [42, 14],
        [52, 11],
        [88, 11],
        [98, 25],
        [108, 5],
        [122, 5],
        [126, 12],
        [148, 6],
        [152, 0],
        [154, 0],
        [160, 16],
        [174, 20],
        [178, 0],
        [194, 0],
        [198, 4],
        [210, 4],
        [216, 15],
        [230, 24],
        [266, 24],
        [274, 12],
        [283, 12],
        [296, 24],
        [326, 24],
        [336, 17],
        [360, 32],
        [380, 8],
        [400, 8],
        [430, 0],
        [455, 20],
        [460, 10],
        [500, 0]],
    'unobstructed': [
        [0, 0],
        [10, 15],
        [30, 15],
        [38, 46],
        [66, 30],
        [70, 0],
        [98, 0],
        [101, 27],
        [137, 50],
        [148, 43],
        [152, 0],
        [164, 0],
        [196, 52],
        [200, 0],
        [214, 0],
        [217, 47],
        [240, 47],
        [247, 38],
        [278, 38],
        [286, 15],
        [294, 55],
        [315, 55],
        [325, 40],
        [348, 40],
        [354, 0],
        [363, 10],
        [378, 10],
        [382, 35],
        [400, 35],
        [405, 56],
        [438, 56],
        [440, 40],
        [454, 40],
        [460, 75],
        [490, 0]
    ]
}

# 公路类型与行驶工况的映射关系
highway_type_operation_mode_map = {
    'residential': 'congestion',
    'primary': 'normal',
    'tertiary': 'congestion',
    'secondary': 'unobstructed',
    'trunk': 'congestion',
    'motorway': 'normal',
    'motorway_link': 'normal',
    'primary_link': 'normal',
    'unclassified': 'normal',
    'secondary_link': 'normal',
    'trunk_link': 'normal',
    'living_street': 'normal',
    'tertiary_link': 'normal',
}


# 返回不同状态下的行驶工况
def get_operation_mode_map():
    return operation_mode_map


# 通过各种信息获得对应的行驶工况
def get_operation_mode(highway_type, time_frame=None, season='spring', weather='fine'):
    if type(highway_type).__name__ == 'list':
        return highway_type_operation_mode_map[highway_type[0]]
    return highway_type_operation_mode_map[highway_type]
