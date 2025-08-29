import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
import os

# 设置matplotlib参数
plt.rcParams['font.family'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['figure.dpi'] = 300

# 创建输出目录
os.makedirs('OUT/OUT', exist_ok=True)

# 读取处理后的数据
df = pd.read_csv('11_processed.csv')

# 提取数据
voc_data = df['total_VOC_ppb'].values
nox_data = df['total_NOx_ppb'].values
o3_data = df['O3_ppb'].values

# 创建更精细的网格
voc_min, voc_max = np.percentile(voc_data, [5, 95])
nox_min, nox_max = np.percentile(nox_data, [5, 95])
voc_range = np.linspace(voc_min, voc_max, 100)
nox_range = np.linspace(nox_min, nox_max, 100)
VOC, NOx = np.meshgrid(voc_range, nox_range)

# 插值O3数据
O3_grid = griddata((voc_data, nox_data), o3_data, (VOC, NOx), method='cubic')
O3_smooth = gaussian_filter(O3_grid, sigma=1.5)

# 计算脊线（更准确的方法）
def find_ridge_line(Z):
    """找到脊线（O3最大值轨迹）"""
    ridge_points = []
    for i, voc_val in enumerate(voc_range):
        col = Z[:, i]
        if np.all(np.isnan(col)):
            continue
        max_idx = np.nanargmax(col)
        ridge_points.append([voc_val, nox_range[max_idx], col[max_idx]])
    return np.array(ridge_points)

ridge_points = find_ridge_line(O3_smooth)

# 绘制EKMA曲线
fig, ax = plt.subplots(figsize=(12, 10))

# 绘制等高线
levels = np.linspace(np.nanmin(O3_smooth), np.nanmax(O3_smooth), 15)
contourf = ax.contourf(VOC, NOx, O3_smooth, levels=levels, cmap='viridis', alpha=0.8)
cbar = plt.colorbar(contourf, ax=ax, label='O₃ Concentration (ppb)', shrink=0.8)

contour = ax.contour(VOC, NOx, O3_smooth, levels=levels, colors='white', linewidths=0.5, alpha=0.7)
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.0f')

# 绘制脊线
if len(ridge_points) > 0:
    ax.plot(ridge_points[:, 0], ridge_points[:, 1], 'r-', linewidth=3, label='脊线 (Ridge Line)')
    
    # 标记关键点（使用三角形）
    key_indices = np.linspace(0, len(ridge_points)-1, min(8, len(ridge_points)), dtype=int)
    key_points = ridge_points[key_indices]
    ax.scatter(key_points[:, 0], key_points[:, 1], 
               color='red', marker='^', s=120, 
               edgecolors='black', linewidth=2, 
               label='关键点', zorder=10)

# 判断控制区域
if len(ridge_points) >= 3:
    # 计算脊线斜率
    slopes = np.diff(ridge_points[:, 1]) / np.diff(ridge_points[:, 0])
    avg_slope = np.nanmean(np.abs(slopes))
    
    # 根据斜率判断控制类型
    if avg_slope > 5:
        control_type = "VOC-Limited"
        control_color = "lightcoral"
    elif avg_slope < 1:
        control_type = "NOx-Limited"
        control_color = "lightblue"
    else:
        control_type = "Transition"
        control_color = "lightgreen"
    
    # 添加控制区域标注
    ax.text(0.7, 0.15, f'控制类型: {control_type}', 
            transform=ax.transAxes, fontsize=14,
            bbox=dict(boxstyle="round,pad=0.5", facecolor=control_color, alpha=0.8),
            ha='center', va='center')

    print(f"控制类型: {control_type}")
    print(f"平均斜率: {avg_slope:.2f}")

# 设置标签和标题
ax.set_xlabel('VOC浓度 (ppb)', fontsize=14)
ax.set_ylabel('NOx浓度 (ppb)', fontsize=14)
ax.set_title('EKMA曲线与臭氧生成脊线分析', fontsize=16, pad=20)

# 移除网格线
ax.grid(False)

# 优化图例
ax.legend(loc='upper right', fontsize=12, framealpha=0.01)

# 设置坐标轴范围
ax.set_xlim(voc_min, voc_max)
ax.set_ylim(nox_min, nox_max)

plt.tight_layout()
plt.savefig('OUT/OUT/optimized_ekma_curve.png', dpi=300, bbox_inches='tight')
plt.close()

print("优化的EKMA曲线已保存")

# 创建控制区域分布图
fig, ax = plt.subplots(figsize=(12, 10))

# 散点图，颜色表示VOC/NOx比率
scatter = ax.scatter(df['total_VOC_ppb'], df['total_NOx_ppb'], 
                     c=df['O3_ppb'], s=50, alpha=0.7, cmap='plasma')
cbar = plt.colorbar(scatter, ax=ax, label='O₃浓度 (ppb)', shrink=0.8)

# 添加控制区域边界
if 'control_type' in locals():
    if control_type == "VOC-Limited":
        ax.axvline(x=np.median(df['total_VOC_ppb']), color='r', linestyle='--', alpha=0.5, label='VOC控制边界')
    elif control_type == "NOx-Limited":
        ax.axhline(y=np.median(df['total_NOx_ppb']), color='b', linestyle='--', alpha=0.5, label='NOx控制边界')
    else:
        # Transition region
        pass

ax.set_xlabel('VOC浓度 (ppb)', fontsize=14)
ax.set_ylabel('NOx浓度 (ppb)', fontsize=14)
ax.set_title('VOC-NOx控制区域分布', fontsize=16)
ax.grid(False)
ax.legend(framealpha=0.01)

plt.tight_layout()
plt.savefig('OUT/OUT/control_regions_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("控制区域分布图已保存")
