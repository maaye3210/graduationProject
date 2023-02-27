from sympy import diff
from sympy import symbols
from scipy import integrate

"""
    以下参数为常量
"""
m = 12400  # 整备质量 m/kg
g = 9.8  # 重力加速度 g/（m/s2）
eta_T = 0.9  # 机械传动效率ηT
eta_m = 0.8  # 电机工作效率ηm
eta_b = 0.8  # 电池效率ηb

delta = 1.02  # 汽车旋转质量换算系数 δ
eta_c = 0.8  # 制动回收效率ηc
C_D = 0.67  # 空气阻力系数 CD
A = 7.6  # 迎风面积 A/m2
f = 0.02  # 滚动阻力系数 f

"""
    以下参数为变量
"""
t_1 = 0 / 360  # 加速启动时间
t_2 = 126 / 360  # 停止加速时间
t = t_2 - t_1  # Δt
a = 30  # 加速度


def E_1(t):
    U_a = a * t  # 汽车行驶速度U_a(t)

    def func(t):
        return (delta * m * U_a) / 3600  # 构造式子中需要求导的函数

    t = symbols("t")  # 需要进行求导的变量t
    return 1 / (eta_T * eta_m * eta_b) * ((m * g * f * U_a) / 3600 + (C_D * A * U_a ** 3) / 76140 + diff(func(t), t))


def E_2(t):
    U_a = a * t  # 汽车行驶速度U_a(t)
    return (t_2 - t_1) / (eta_T * eta_m * eta_b) * ((m * g * f * U_a) / 3600 + (C_D * A * U_a ** 3) / 76140)


def E_3(t):
    v_2 = a * t_2  # 末速度
    v_1 = a * t_1  # 初速度
    return (1 / 3.6) ** 3 + ((1 - eta_c) / (10 ** 6 * eta_T * eta_m * eta_b)) * (
            (1 / 2 * m * v_2 ** 2) - (1 / 2 * m * v_1 ** 2))


def get_energy_consumption():
    return integrate.quad(E_1, t_1, t_2)[0] + E_2(t) + E_3(t)


if __name__ == "__main__":
    E1 = integrate.quad(E_1, t_1, t_2)[0]  # E1式子中求积分
    E2 = E_2(t)  # 求E2
    E3 = E_3(t)  # 求E3
    E = E1 + E2 + E3  # 求E
    print(f"E = {E}")  # 输出E
