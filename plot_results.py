import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = np.loadtxt('model/output/speciesConcentrations.output', skiprows=1)
time = data[:, 0]
ch4 = data[:, 1]
o3 = data[:, 3]
no2 = data[:, 4]
no = data[:, 5]
oh = data[:, 6]
ho2 = data[:, 7]

# 创建图形
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(time, ch4)
plt.title('CH4 Concentration')
plt.xlabel('Time (s)')
plt.ylabel('Concentration')

plt.subplot(2, 2, 2)
plt.plot(time, o3)
plt.title('O3 Concentration')
plt.xlabel('Time (s)')
plt.ylabel('Concentration')

plt.subplot(2, 2, 3)
plt.plot(time, no, label='NO')
plt.plot(time, no2, label='NO2')
plt.title('NO and NO2 Concentration')
plt.xlabel('Time (s)')
plt.ylabel('Concentration')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(time, oh, label='OH')
plt.plot(time, ho2, label='HO2')
plt.title('OH and HO2 Concentration')
plt.xlabel('Time (s)')
plt.ylabel('Concentration')
plt.legend()

plt.tight_layout()
plt.savefig('species_concentrations.png')
print("图形已保存为 species_concentrations.png")
