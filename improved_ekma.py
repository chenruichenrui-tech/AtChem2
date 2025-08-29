import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import matplotlib.font_manager as fm

# 设置字体 - 使用支持中文的字体
plt.rcParams['font.family'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取转换后的11.csv文件
df = pd.read_csv('11_english.csv')

# 创建OUT/OUT子目录
import os
os.makedirs('OUT/OUT', exist_ok=True)

# 提取VOC、NOx和O3数据
voc_data = df['total_VOC_ppb'].values
nox_data = df['total_NOx_ppb'].values
o3_data = df['O3_ppb'].values

# 创建VOC和NOx浓度网格
voc_range = np.linspace(np.min(voc_data), np.max(voc_data), 50)
nox_range = np.linspace(np.min(nox_data), np.max(nox_data), 50)
VOC, NOx = np.meshgrid(voc_range, nox_range)

# 插值O3浓度数据到网格
O3_max = griddata(
    (voc_data, nox_data), 
    o3_data, 
    (VOC, NOx), 
    method='linear'
)

# 应用高斯滤波平滑数据
O3_max_smooth = gaussian_filter(O3_max, sigma=1.5)

# 绘制改进的EKMA曲线
plt.figure(figsize=(12, 10))

# 绘制填充等高线
contourf = plt.contourf(VOC, NOx, O3_max_smooth, levels=20, cmap='viridis', alpha=0.8)
plt.colorbar(contourf, label='O₃ Concentration (ppb)')

# 绘制等高线
contour = plt.contour(VOC, NOx, O3_max_smooth, levels=15, colors='black', linewidths=1)
plt.clabel(contour, inline=True, fontsize=9, fmt='%1.0f')

# 计算并绘制脊线（O3最大值的轨迹）
ridge_line = []
for i in range(len(voc_range)):
    max_idx = np.argmax(O3_max_smooth[:, i])
    ridge_line.append((voc_range[i], nox_range[max_idx]))

ridge_line = np.array(ridge_line)

# 标记脊线上的关键点（使用三角形）
key_points = []
for i in range(0, len(ridge_line), 5):  # 每5个点选一个关键点
    key_points.append(ridge_line[i])
key_points = np.array(key_points)

plt.plot(ridge_line[:, 0], ridge_line[:, 1], 'r--', linewidth=2, label='Ridge Line')
plt.scatter(key_points[:, 0], key_points[:, 1], color='red', marker='^', s=100, 
            edgecolors='black', linewidth=1, label='Key Points', zorder=5)

# 确定控制区域
# 计算脊线的斜率变化
slopes = np.diff(ridge_line[:, 1]) / np.diff(ridge_line[:, 0])
avg_slope = np.mean(np.abs(slopes))

# 根据平均斜率判断控制类型
if avg_slope < 0.5:
    control_type = "NOx-Limited"
    control_text = "NOx-Limited Region"
    text_x = np.percentile(voc_range, 70)
    text_y = np.percentile(nox_range, 30)
elif avg_slope > 2:
    control_type = "VOC-Limited"
    control_text = "VOC-Limited Region"
    text_x = np.percentile(voc_range, 30)
    text_y = np.percentile(nox_range, 70)
else:
    control_type = "Transition"
    control_text = "Transition Region"
    text_x = np.percentile(voc_range, 50)
    text_y = np.percentile(nox_range, 50)

# 添加控制区域文本
plt.text(text_x, text_y, control_text, fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
         ha='center', va='center')

plt.xlabel('VOC Concentration (ppb)', fontsize=12)
plt.ylabel('NOx Concentration (ppb)', fontsize=12)
plt.title('EKMA Curve with Ridge Line and Control Regions', fontsize=14)
plt.legend(loc='upper right', fontsize=10, framealpha=0.01)
plt.grid(False)  # 移除网格线

# 保存图像
plt.tight_layout()
plt.savefig('OUT/OUT/improved_ekma_curve.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"改进的EKMA曲线已保存，控制类型: {control_type}")
print(f"脊线平均斜率: {avg_slope:.3f}")

# 创建控制区域分布图
plt.figure(figsize=(10, 8))

# 根据VOC/NOx比率着色
colors = df['VOC_NOx_ratio']
scatter = plt.scatter(df['total_VOC_ppb'], df['total_NOx_ppb'], 
                     c=colors, cmap='coolwarm', alpha=0.7, s=30)
plt.colorbar(scatter, label='VOC/NOx Ratio')

# 添加控制区域边界（示意）
if control_type == "NOx-Limited":
    # 在低NOx区域添加文本
    plt.text(np.percentile(voc_range, 70), np.percentile(nox_range, 20), 
             "NOx-Limited", fontsize=12, ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
elif control_type == "VOC-Limited":
    # 在低VOC区域添加文本
    plt.text(np.percentile(voc_range, 20), np.percentile(nox_range, 70), 
             "VOC-Limited", fontsize=12, ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
else:
    # 在中间区域添加文本
    plt.text(np.percentile(voc_range, 50), np.percentile(nox_range, 50), 
             "Transition", fontsize=12, ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))

plt.xlabel('VOC Concentration (ppb)', fontsize=12)
plt.ylabel('NOx Concentration (ppb)', fontsize=12)
plt.title('O₃ Control Regions based on VOC/NOx Ratio', fontsize=14)
plt.legend([], [], frameon=False)
plt.grid(False)  # 移除网格线

# 保存图像
plt.tight_layout()
plt.savefig('OUT/OUT/control_regions.png', dpi=300, bbox_inches='tight')
plt.close()

print("控制区域分布图已保存")
