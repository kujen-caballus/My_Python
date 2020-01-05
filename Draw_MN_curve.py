import numpy as np
import matplotlib.pyplot as plt

width = 0.5
height = 0.5

height_to_steel_dt = 0.05
height_to_steel_dt2 = height - height_to_steel_dt
height_to_steel_dc = 0.05
height_to_steel_dc2 = height - height_to_steel_dc

height_ratio_dt1 = height_to_steel_dt / height
height_ratio_dc1 = height_to_steel_dc / height
height_ratio_d1 = 1.0 - height_ratio_dc1

F_concrete = 24.0
F_steel = 215.0

f_concrete_long = F_concrete * 0.333
f_steel_long = 195.0

f_concrete_short = F_concrete * 0.333
f_steel_short = 390.0

axial_force_n = 500.0
elastic_modules_steel = 205000.0
elastic_modules_concrete = 22600.0
elastic_ratio = elastic_modules_steel / elastic_modules_concrete
elastic_ratio_m = elastic_ratio - 1.0

steel_total_area = 0.001267
steel_ratio = 0.005

x_n1 = np.arange(0.1, 3.05, 0.05)





x_n1b = height_ratio_d1 / (1.0 + (1 / elastic_ratio) * (f_steel_long / f_concrete_long))

M = []
N = []
for i in x_n1:
    if i < x_n1b:
        i = (f_steel_long / (elastic_ratio * (height_ratio_d1 - i))) * (0.0833 * i * i * (3 - 2 * i) + steel_ratio*(0.5 - height_ratio_dc1) * (
                elastic_ratio_m * (i - height_ratio_dc1) + elastic_ratio * (height_ratio_d1 - i)))
    elif (x_n1b <= i) & (i <= 1.0):
        i = (0.0833 * i * (3 - 2 * i) + (((steel_ratio / i) * (0.5 - height_ratio_dt1)) * (elastic_ratio_m * (
                i - height_ratio_dc1) + (elastic_ratio * (height_ratio_d1 - i))))) * f_concrete_long
    elif 1.0 < i:
        i = (0.5 * f_concrete_long / i) * (0.166 + elastic_ratio_m * steel_ratio * ((1.0 - 2.0 * height_ratio_dt1) * (
                1.0 - 2.0 * height_ratio_dt1)))
    M.append(i)

for i in x_n1:
    if i < x_n1b:
        i = (f_steel_long / (elastic_ratio * (height_ratio_d1 - i))) * ((0.5 * i * i) + (steel_ratio * (
            (elastic_ratio_m * (i - height_ratio_dc1)) - (elastic_ratio * (
                height_ratio_d1 - i)))))
    elif (x_n1b <= i) & (i <= 1.0):
        i = (0.5 * i + ((steel_ratio / i) * (elastic_ratio_m * (i - height_ratio_dc1) - elastic_ratio * (
                height_ratio_d1 - i)))) * f_concrete_long
    elif 1.0 < i:
        i = (1 + 2 * elastic_ratio_m * steel_ratio) * (1.0 - (0.5 / i)) * f_concrete_long
    N.append(i)


M1 = np.array(M)
N1 = np.array(N)

print(x_n1b)
print(M1)
print(N1)

plt.plot(M1,N1)
plt.show()