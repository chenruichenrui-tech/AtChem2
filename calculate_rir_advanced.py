import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# 读取模拟结果
try:
    df = pd.read_csv('ekma_simulation_results.csv')
    print(f"成功读取模拟结果，包含 {len(df)} 行数据")
except Exception as e:
    print(f"读取模拟结果失败: {e}")
    exit(1)

# 计算VOC/NOx比率
df['VOC_NOx_ratio'] = df['VOC_conc'] / df['NOx_conc']

# 计算RIR（相对增量反应性）
# 首先，找到基准案例（例如，VOC/NOx = 8）
if 'VOC_NOx_ratio' in df.columns:
    base_idx = (df['VOC_NOx_ratio'] - 8).abs().argsort()[:1].values[0]
    base_o3 = df.loc[base_idx, 'O3_max']
    
    # 计算每个案例相对于基准案例的RIR
    df['RIR'] = df['O3_max'] / base_o3
    
    # 保存RIR结果
    df.to_csv('rir_advanced_results.csv', index=False)
    
    # 绘制RIR柱状图
    plt.figure(figsize=(12, 8))
    
    # 计算不同VOC/NOx比率范围内的平均RIR
    ratio_bins = np.linspace(df['VOC_NOx_ratio'].min(), df['VOC_NOx_ratio'].max(), 10)
    df['ratio_bin'] = pd.cut(df['VOC_NOx_ratio'], bins=ratio_bins)
    
    # 计算每个bin的平均RIR
    mean_rir = df.groupby('ratio_bin')['RIR'].mean()
    
    # 绘制柱状图
    plt.bar(range(len(mean_rir)), mean_rir.values)
    plt.xlabel('VOC/NOx Ratio Bin')
    plt.ylabel('Average Relative Incremental Reactivity (RIR)')
    plt.title('Average RIR by VOC/NOx Ratio')
    plt.xticks(range(len(mean_rir)), [f'{b.left:.1f}-{b.right:.1f}' for b in mean_rir.index], rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('rir_bar_chart.png', dpi=300)
    plt.close()
    
    print("RIR计算完成，结果已保存到 rir_advanced_results.csv 和 rir_bar_chart.png")
else:
    print("无法计算RIR，缺少VOC/NOx比率数据")
