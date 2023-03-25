from modal.operating_mode import get_operation_mode_map
from modal.modals import ElectricVehicle

conditions = get_operation_mode_map()

if __name__ == "__main__":
    modal = ElectricVehicle(
        name='test',
        m=12400,  # 整备质量 m/kg
        eta_T=0.9,  # 机械传动效率ηT
        eta_m=0.8,  # 电机工作效率ηm
        eta_b=0.8,  # 电池效率ηb
        delta=1.02,  # 汽车旋转质量换算系数 δ
        eta_c=0.8,  # 制动回收效率ηc
        C_D=0.67,  # 空气阻力系数 CD
        A=7.6,  # 迎风面积 A/m2
        f=0.02,  # 滚动阻力系数 f
        k=0.2  # 电气制动比例
    )
    modal.get_average_consumption(conditions)
