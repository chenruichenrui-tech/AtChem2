import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取处理后的数据
try:
    df = pd.read_csv('processed_timeseries.csv')
    print(f"使用processed_timeseries.csv，包含 {len(df)} 行数据")
    # 假设O3最大值在"茅山头O3"列
    o3_col = '茅山头O3'
    df['O3_max'] = df[o3_col]
except Exception as e:
    print(f"读取processed_timeseries.csv失败: {e}")
    exit(1)

# 计算VOC/NOx比率
if '总VOC' in df.columns and 'NOx' in df.columns:
    df['VOC_NOx_ratio'] = df['总VOC'] / df['NOx']
else:
    print("无法计算VOC/NOx比率，缺少必要的列")
    exit(1)

# 计算RIR（相对增量反应性）
# 首先，找到基准案例（例如，VOC/NOx = 8）
if 'VOC_NOx_ratio' in df.columns:
    base_idx = (df['VOC_NOx_ratio'] - 8).abs().argsort()[:1].values[0]
    base_o3 = df.loc[base_idx, 'O3_max']
    
    # 计算每个案例相对于基准案例的RIR
    df['RIR'] = df['O3_max'] / base_o3
    
    # 保存RIR结果
    df.to_csv('rir_results.csv', index=False)
    
    # 绘制RIR曲线
    plt.figure(figsize=(10, 6))
    plt.plot(df['VOC_NOx_ratio'], df['RIR'], 'o-')
    plt.xlabel('VOC/NOx Ratio')
    plt.ylabel('Relative Incremental Reactivity (RIR)')
    plt.title('Relative Incremental Reactivity')
    plt.grid(True)
    plt.savefig('rir_curve.png', dpi=300)
    plt.close()
    
    print("RIR计算完成，结果已保存到 rir_results.csv 和 rir_curve.png")
else:
    print("无法计算RIR，缺少VOC/NOx比率数据")
