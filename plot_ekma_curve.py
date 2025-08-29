import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# 读取处理后的数据
try:
    df = pd.read_csv('processed_timeseries.csv')
    print(f"使用processed_timeseries.csv，包含 {len(df)} 行数据")
    # 假设O3最大值在"茅山头O3"列
    o3_col = '茅山头O3'
    df['O3_max'] = df[o3_col]
    # 使用总VOC和NOx列
    if '总VOC' in df.columns and 'NOx' in df.columns:
        df['VOC_conc'] = df['总VOC']
        df['NOx_conc'] = df['NOx']
    else:
        print("无法找到VOC和NOx浓度数据")
        exit(1)
except Exception as e:
    print(f"读取processed_timeseries.csv失败: {e}")
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
    
    # 绘制EKMA曲线（等高线图）
    plt.figure(figsize=(10, 8))
    contour = plt.contour(VOC, NOx, O3_max, levels=15, colors='black')
    plt.clabel(contour, inline=True, fontsize=8)
    plt.contourf(VOC, NOx, O3_max, levels=15, cmap='RdYlBu_r')
    plt.colorbar(label='O3 Maximum Concentration')
    plt.xlabel('VOC Concentration')
    plt.ylabel('NOx Concentration')
    plt.title('EKMA Curve - O3 Isopleths')
    plt.grid(True)
    plt.savefig('ekma_curve.png', dpi=300)
    plt.close()
    
    print("EKMA曲线已保存为 ekma_curve.png")
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
