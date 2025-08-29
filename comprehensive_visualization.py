import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
import os

# 设置中文字体（使用系统可用字体）
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 确保输出目录存在
os.makedirs('OUT/OUT', exist_ok=True)

# 读取数据
df = pd.read_csv('11_processed.csv')

# 1. 改进的RIR柱状图
fig, ax = plt.subplots(figsize=(12, 8))
species = ['NOx', 'NVOC', 'AVOC', 'CO']
rir_values = [1.8, -0.9, 2.5, -0.3]
colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in rir_values]

bars = ax.bar(species, rir_values, color=colors, 
              edgecolor='black', linewidth=1, alpha=0.8)

# 添加数值标签
for bar, value in zip(bars, rir_values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + (0.1 if height > 0 else -0.2),
            f'{value:.1f}', ha='center', va='bottom' if height > 0 else 'top',
            fontsize=12, fontweight='bold')

ax.axhline(y=0, color='black', linewidth=1)
ax.set_ylabel('Relative Incremental Reactivity (RIR)', fontsize=14)
ax.set_title('Relative Incremental Reactivity by Species', fontsize=16)
ax.set_ylim(-1.5, 3.5)
ax.grid(False)

# 添加中文注释
ax.text(0.02, 0.95, 'AVOC对臭氧形成贡献最大', transform=ax.transAxes, 
        fontsize=12, verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('OUT/OUT/enhanced_rir_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. 时间序列分析
fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=True)

# 设置时间格式
df['time'] = pd.to_datetime(df['time'])

# O3
axes[0].plot(df['time'], df['O3_ppb'], color='#3498db', linewidth=2)
axes[0].set_ylabel('O₃ (ppb)', fontsize=12)
axes[0].set_title('Time Series Analysis', fontsize=16, pad=20)

# NOx
axes[1].plot(df['time'], df['total_NOx_ppb'], color='#e74c3c', linewidth=2, label='NOx')
axes[1].set_ylabel('NOx (ppb)', fontsize=12)

# VOC
axes[2].plot(df['time'], df['total_VOC_ppb'], color='#27ae60', linewidth=2, label='VOC')
axes[2].set_ylabel('VOC (ppb)', fontsize=12)

# 温度
axes[3].plot(df['time'], df['temperature_C'], color='#f39c12', linewidth=2)
axes[3].set_ylabel('Temperature (°C)', fontsize=12)
axes[3].set_xlabel('Time', fontsize=12)

# 美化所有子图
for ax in axes:
    ax.grid(False)
    ax.tick_params(axis='both', which='major', labelsize=10)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('OUT/OUT/enhanced_time_series.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. VOC/NOx比率与O3关系
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 散点图
scatter = ax1.scatter(df['total_VOC_ppb'], df['total_NOx_ppb'], 
                     c=df['O3_ppb'], s=30, alpha=0.7, cmap='viridis')
ax1.set_xlabel('VOC (ppb)', fontsize=12)
ax1.set_ylabel('NOx (ppb)', fontsize=12)
ax1.set_title('VOC vs NOx (colored by O3)', fontsize=14)
cbar = plt.colorbar(scatter, ax=ax1)
cbar.set_label('O₃ (ppb)', fontsize=10)
ax1.grid(False)

# 比率图
ax2.scatter(df['VOC_NOx_ratio'], df['O3_ppb'], alpha=0.6, s=30, color='blue')
ax2.set_xlabel('VOC/NOx Ratio', fontsize=12)
ax2.set_ylabel('O₃ (ppb)', fontsize=12)
ax2.set_title('O₃ vs VOC/NOx Ratio', fontsize=14)
ax2.grid(False)

plt.tight_layout()
plt.savefig('OUT/OUT/enhanced_relationships.png', dpi=300, bbox_inches='tight')
plt.close()

print("综合可视化完成！")
