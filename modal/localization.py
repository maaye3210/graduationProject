import osmnx as ox
from modal.operating_mode import get_operation_mode_map
from modal.modals import TraditionalVehicle, ElectricVehicle, Modal

print('start')
file_path = '../demtest/huancui_with_dem.graphml'

# 获取道路数据
G = ox.load_graphml(file_path)

# 获取不同工况
conditions = get_operation_mode_map()

# 预设模型
# 传统汽车模型
traditional_modal = TraditionalVehicle(
    name='traditional',
    m=12400,  # 整备质量 m/kg
    eta_T=0.9,  # 机械传动效率ηT
    delta=1.02,  # 汽车旋转质量换算系数 δ
    C_D=0.67,  # 空气阻力系数 CD
    A=2.6,  # 迎风面积 A/m2
    f=0.02,  # 滚动阻力系数 f
    k=0.2  # 电气制动比例
)

# 电动汽车模型
electric_modal = ElectricVehicle(
    name='electric',
    m=12400,  # 整备质量 m/kg
    eta_T=0.9,  # 机械传动效率ηT
    eta_m=0.8,  # 电机工作效率ηm
    eta_b=0.8,  # 电池效率ηb
    delta=1.02,  # 汽车旋转质量换算系数 δ
    eta_c=0.8,  # 制动回收效率ηc
    C_D=0.67,  # 空气阻力系数 CD
    A=2.6,  # 迎风面积 A/m2
    f=0.02,  # 滚动阻力系数 f
    k=0.2  # 电气制动比例
)

# 默认模型，只能计算最短路径
default_modal = Modal('default')
traditional_modal.localization()
electric_modal.localization()
modal_list = [traditional_modal, electric_modal]

