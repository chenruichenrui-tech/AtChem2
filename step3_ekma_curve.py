import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os

# 设置字体
plt.rcParams['font.family'] = 'DejaVu Sans'

# 读取处理后的数据
df = pd.read_csv('OUT/11_processed.csv')

# 清除缺失值
df_clean = df.dropna(subset=['total_VOC_ppb', 'total_NOx_ppb', 'O3_ppb'])

voc = df_clean['total_VOC_ppb']
nox = df_clean['total_NOx_ppb']
o3 = df_clean['O3_ppb']

print(f"VOC范围: {voc.min():.2f} - {voc.max():.2f} ppb")
print(f"NOx范围: {nox.min():.2f} - {nox.max():.2f} ppb")
print(f"O3范围: {o3.min():.2f} - {o3.max():.2f} ppb")

# 创建网格
v = np.linspace(voc.min(), voc.max(), 100)
n = np.linspace(nox.min(), nox.max(), 100)
V, N = np.meshgrid(v, n)

# 插值计算O3浓度
Z = griddata((voc, nox), o3, (V, N), method='linear')

# 改进的脊线检测方法
ridge_points = []
for i, v_val in enumerate(v):
    # 找到当前VOC值下O3最大值对应的NOx
    col = Z[:, i]
    if not np.all(np.isnan(col)):
        max_o3_idx = np.nanargmax(col)
        ridge_points.append([v_val, n[max_o3_idx]])

ridge = np.array(ridge_points)

# 计算脊线斜率
if len(ridge) > 1:
    slopes = np.diff(ridge[:, 1]) / np.diff(ridge[:, 0])
    mean_slope = np.nanmean(np.abs(slopes))
    
    # 根据斜率判断控制区域
    if mean_slope > 2.0:
        regime = 'VOC-Limited'
        color = 'red'
    elif mean_slope < 0.5:
        regime = 'NOx-Limited'
        color = 'blue'
    else:
        regime = 'Transition'
        color = 'purple'
else:
    regime = 'Undetermined'
    color = 'gray'

print(f"控制区域: {regime}")
print(f"脊线平均斜率: {mean_slope if len(ridge) > 1 else 'N/A'}")

# 绘制EKMA曲线
fig, ax = plt.subplots(figsize=(12, 9))
cs = ax.contourf(V, N, Z, levels=20, cmap='viridis')
plt.colorbar(cs, label='O3 (ppb)')

# 绘制脊线
if len(ridge) > 1:
    ax.plot(ridge[:, 0], ridge[:, 1], 'r-', linewidth=2, label='Ridge Line')
    ax.scatter(ridge[::3, 0], ridge[::3, 1], marker='^', s=100, color='yellow', edgecolors='k')

# 添加控制区域标注
ax.text(0.75, 0.15, regime, transform=ax.transAxes,
        bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.7),
        fontsize=12, color='white', ha='center')

ax.set_xlabel('VOC (ppb)')
ax.set_ylabel('NOx (ppb)')
ax.set_title('EKMA Curve and Control Regime')
ax.grid(True, alpha=0.3)
if len(ridge) > 1:
    ax.legend()

# 保存图表
plt.tight_layout()
plt.savefig('OUT/FINAL/improved_ekma_curve.png')
plt.close()

print("✅ 步骤3完成: EKMA曲线绘制")
