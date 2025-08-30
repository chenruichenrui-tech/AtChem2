import pandas as pd
import numpy as np

# 读取处理后的数据
df = pd.read_csv('OUT/11_processed.csv')

print("="*50)
print("数据分析汇总报告")
print("="*50)

# 基本统计信息
print("\n1. 基本统计信息:")
print(f"数据时间段: {df['time'].min()} 至 {df['time'].max()}")
print(f"O3浓度范围: {df['O3_ppb'].min():.2f} - {df['O3_ppb'].max():.2f} ppb")
print(f"VOC浓度范围: {df['total_VOC_ppb'].min():.2f} - {df['total_VOC_ppb'].max():.2f} ppb")
print(f"NOx浓度范围: {df['total_NOx_ppb'].min():.2f} - {df['total_NOx_ppb'].max():.2f} ppb")

# 相关性分析
print("\n2. 相关性分析:")
correlation = df[['O3_ppb', 'total_VOC_ppb', 'total_NOx_ppb', 'temperature_C']].corr()
print("O3与各参数的相关性:")
print(f"  O3-VOC: {correlation.loc['O3_ppb', 'total_VOC_ppb']:.3f}")
print(f"  O3-NOx: {correlation.loc['O3_ppb', 'total_NOx_ppb']:.3f}")
print(f"  O3-温度: {correlation.loc['O3_ppb', 'temperature_C']:.3f}")

# 高臭氧事件分析
high_o3_threshold = df['O3_ppb'].quantile(0.9)
high_o3_days = df[df['O3_ppb'] > high_o3_threshold]
print(f"\n3. 高臭氧事件分析 (阈值: {high_o3_threshold:.2f} ppb):")
print(f"  高臭氧事件次数: {len(high_o3_days)}")
if len(high_o3_days) > 0:
    print(f"  高臭氧期间平均VOC: {high_o3_days['total_VOC_ppb'].mean():.2f} ppb")
    print(f"  高臭氧期间平均NOx: {high_o3_days['total_NOx_ppb'].mean():.2f} ppb")
    print(f"  高臭氧期间平均温度: {high_o3_days['temperature_C'].mean():.2f} °C")

# VOC/NOx比率分析
df['VOC_NOx_ratio'] = df['total_VOC_ppb'] / df['total_NOx_ppb']
print(f"\n4. VOC/NOx比率分析:")
print(f"  平均比率: {df['VOC_NOx_ratio'].mean():.2f}")
print(f"  比率范围: {df['VOC_NOx_ratio'].min():.2f} - {df['VOC_NOx_ratio'].max():.2f}")

# 根据比率判断臭氧生成敏感性
ratio_threshold_low = 4  # 低于此值为NOx控制区
ratio_threshold_high = 10  # 高于此值为VOC控制区

nox_limited = df[df['VOC_NOx_ratio'] > ratio_threshold_high]
voc_limited = df[df['VOC_NOx_ratio'] < ratio_threshold_low]
transition = df[(df['VOC_NOx_ratio'] >= ratio_threshold_low) & (df['VOC_NOx_ratio'] <= ratio_threshold_high)]

print(f"\n5. 基于VOC/NOx比率的臭氧生成敏感性:")
print(f"  NOx控制区 (比率 > {ratio_threshold_high}): {len(nox_limited)} 个样本")
print(f"  VOC控制区 (比率 < {ratio_threshold_low}): {len(voc_limited)} 个样本")
print(f"  过渡区: {len(transition)} 个样本")

print("\n6. 分析结果已保存至:")
print("  - OUT/11_processed.csv (处理后的数据)")
print("  - OUT/FINAL/improved_rir_chart.png (RIR图表)")
print("  - OUT/FINAL/improved_ekma_curve.png (EKMA曲线)")
print("  - OUT/FINAL/time_series.png (时间序列)")
print("  - OUT/FINAL/relationships.png (关系图)")

print("\n✅ 步骤5完成: 汇总报告生成")
