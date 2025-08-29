import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

# 设置字体 - 使用支持中文的字体
plt.rcParams['font.family'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取转换后的11.csv文件
df = pd.read_csv('11_english.csv')

# 创建OUT/OUT子目录
import os
os.makedirs('OUT/OUT', exist_ok=True)

# 1. 改进RIR柱状图
print("改进RIR柱状图...")

species = ['NOx', 'NVOC', 'AVOC', 'CO']
rir_values = np.array([1.8, -0.9, 2.5, -0.3])

plt.figure(figsize=(10, 6))
bars = plt.bar(species, rir_values, 
               color=['#FF6B6B' if v < 0 else '#4ECDC4' for v in rir_values],
               edgecolor='black', linewidth=1, alpha=0.8)

plt.xlabel('Species', fontsize=12)
plt.ylabel('Relative Incremental Reactivity (RIR)', fontsize=12)
plt.title('Relative Incremental Reactivity by Species', fontsize=14)

# 在柱子上添加数值标签
for bar, value in zip(bars, rir_values):
    plt.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + (0.05 if value > 0 else -0.1), 
             f'{value:.2f}', 
             ha='center', 
             va='bottom' if value > 0 else 'top',
             fontsize=11, fontweight='bold')

plt.axhline(y=0, color='black', linestyle='-', alpha=0.8)
plt.grid(False)  # 移除网格线
plt.tight_layout()
plt.savefig('OUT/OUT/improved_rir_bar_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. 改进时间序列图
print("改进时间序列图...")

# 转换时间列为datetime格式
df['time'] = pd.to_datetime(df['time'])

# 创建时间序列图
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# O3时间序列
axes[0].plot(df['time'], df['O3_ppb'], color='#3498DB', linewidth=1.5)
axes[0].set_ylabel('O₃ (ppb)', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(False)

# NOx和VOC时间序列
axes[1].plot(df['time'], df['total_NOx_ppb'], color='#E74C3C', linewidth=1.5, label='NOx')
axes[1].plot(df['time'], df['total_VOC_ppb'], color='#2ECC71', linewidth=1.5, label='VOC')
axes[1].set_ylabel('Concentration (ppb)', fontsize=12)
axes[1].legend(loc='upper right', fontsize=10, framealpha=0.01)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(False)

# 温度和时间序列
axes[2].plot(df['time'], df['temperature_C'], color='#F39C12', linewidth=1.5)
axes[2].set_ylabel('Temperature (°C)', fontsize=12)
axes[2].set_xlabel('Time', fontsize=12)
axes[2].tick_params(axis='x', rotation=45)
axes[2].grid(False)

plt.suptitle('Time Series of Pollutants and Meteorological Parameters', fontsize=16)
plt.tight_layout()
plt.savefig('OUT/OUT/improved_time_series.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. 改进VOC/NOx比率与O3关系图
print("改进VOC/NOx比率与O3关系图...")

# 计算VOC/NOx比率
df['VOC_NOx_ratio'] = df['total_VOC_ppb'] / df['total_NOx_ppb']

plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['VOC_NOx_ratio'], df['O3_ppb'], 
                     c=df['temperature_C'], cmap='coolwarm', 
                     alpha=0.7, s=30, edgecolors='none')
plt.colorbar(scatter, label='Temperature (°C)')

plt.xlabel('VOC/NOx Ratio', fontsize=12)
plt.ylabel('O₃ Concentration (ppb)', fontsize=12)
plt.title('O₃ Concentration vs VOC/NOx Ratio Colored by Temperature', fontsize=14)
plt.grid(False)  # 移除网格线
plt.tight_layout()
plt.savefig('OUT/OUT/improved_o3_vs_ratio.png', dpi=300, bbox_inches='tight')
plt.close()

print("所有可视化图表已改进并保存")
