import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

# 读取模拟结果
try:
    df = pd.read_csv('ekma_simulation_results.csv')
    print(f"成功读取模拟结果，包含 {len(df)} 行数据")
except Exception as e:
    print(f"读取模拟结果失败: {e}")
    exit(1)

# 创建网格用于等高线图
voc_values = np.unique(df['VOC_conc'])
nox_values = np.unique(df['NOx_conc'])

if len(voc_values) > 1 and len(nox_values) > 1:
    # 创建网格
    VOC, NOx = np.meshgrid(voc_values, nox_values)
    
    # 插值O3最大值到网格
    O3_max = griddata(
        (df['VOC_conc'], df['NOx_conc']), 
        df['O3_max'], 
        (VOC, NOx), 
        method='cubic'
    )
    
    # 应用高斯滤波平滑数据
    O3_max_smooth = gaussian_filter(O3_max, sigma=1)
    
    # 绘制EKMA曲线（等高线图）
    plt.figure(figsize=(12, 10))
    contour = plt.contour(VOC, NOx, O3_max_smooth, levels=15, colors='black')
    plt.clabel(contour, inline=True, fontsize=8)
    
    # 绘制填充等高线
    contourf = plt.contourf(VOC, NOx, O3_max_smooth, levels=15, cmap='RdYlBu_r')
    plt.colorbar(contourf, label='O3 Maximum Concentration')
    
    # 计算并绘制脊线（O3最大值的轨迹）
    # 对于每个VOC浓度，找到使O3最大的NOx浓度
    ridge_line = []
    for i in range(len(voc_values)):
        max_idx = np.argmax(O3_max_smooth[:, i])
        ridge_line.append((voc_values[i], nox_values[max_idx]))
    
    ridge_line = np.array(ridge_line)
    plt.plot(ridge_line[:, 0], ridge_line[:, 1], 'r--', linewidth=2, label='Ridge Line')
    
    plt.xlabel('VOC Concentration')
    plt.ylabel('NOx Concentration')
    plt.title('EKMA Curve - O3 Isopleths with Ridge Line')
    plt.legend()
    plt.grid(True)
    plt.savefig('ekma_curve_advanced.png', dpi=300)
    plt.close()
    
    print("改进的EKMA曲线已保存为 ekma_curve_advanced.png")
else:
    print("数据点不足，无法创建EKMA曲线。需要更多的VOC和NOx浓度组合。")
    
    # 绘制简单的散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(df['VOC_conc'], df['NOx_conc'], c=df['O3_max'], cmap='viridis')
    plt.colorbar(label='O3 Maximum Concentration')
    plt.xlabel('VOC Concentration')
    plt.ylabel('NOx Concentration')
    plt.title('O3 Maximum Concentration vs VOC and NOx')
    plt.grid(True)
    plt.savefig('o3_scatter.png', dpi=300)
    plt.close()
    
    print("已创建O3浓度散点图 o3_scatter.png")
