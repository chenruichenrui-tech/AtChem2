import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("分析AtChem2输出结果...")

# 读取AtChem2输出
output_file = 'atchem2_output/output.csv'
if not os.path.exists(output_file):
    print("❌ AtChem2输出文件不存在")
    exit(1)

df_atchem = pd.read_csv(output_file)

# 转换时间单位为小时
df_atchem['time_hours'] = df_atchem['time'] / 3600

# 绘制主要物种的时间序列
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# O3浓度
axes[0, 0].plot(df_atchem['time_hours'], df_atchem['O3'])
axes[0, 0].set_xlabel('Time (hours)')
axes[0, 0].set_ylabel('O3 (ppb)')
axes[0, 0].set_title('O3 Concentration')
axes[0, 0].grid(True, alpha=0.3)

# NOx浓度
axes[0, 1].plot(df_atchem['time_hours'], df_atchem['NO'], label='NO')
axes[0, 1].plot(df_atchem['time_hours'], df_atchem['NO2'], label='NO2')
axes[0, 1].set_xlabel('Time (hours)')
axes[0, 1].set_ylabel('Concentration (ppb)')
axes[0, 1].set_title('NOx Concentration')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 自由基浓度
if 'OH' in df_atchem.columns:
    axes[1, 0].plot(df_atchem['time_hours'], df_atchem['OH'], label='OH')
if 'HO2' in df_atchem.columns:
    axes[1, 0].plot(df_atchem['time_hours'], df_atchem['HO2'], label='HO2')
if 'RO2' in df_atchem.columns:
    axes[1, 0].plot(df_atchem['time_hours'], df_atchem['RO2'], label='RO2')
axes[1, 0].set_xlabel('Time (hours)')
axes[1, 0].set_ylabel('Concentration (ppt)')
axes[1, 0].set_title('Radical Concentration')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_yscale('log')

# O3生成速率分析
# 计算净O3生成速率 (dO3/dt)
df_atchem['dO3_dt'] = np.gradient(df_atchem['O3'], df_atchem['time'])

axes[1, 1].plot(df_atchem['time_hours'], df_atchem['dO3_dt'])
axes[1, 1].set_xlabel('Time (hours)')
axes[1, 1].set_ylabel('dO3/dt (ppb/s)')
axes[1, 1].set_title('O3 Production Rate')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('OUT/FINAL/atchem2_results.png', dpi=300, bbox_inches='tight')
plt.close()

# 计算关键指标
max_o3 = df_atchem['O3'].max()
max_o3_time = df_atchem.loc[df_atchem['O3'].idxmax(), 'time_hours']
avg_oh = df_atchem['OH'].mean() if 'OH' in df_atchem.columns else np.nan

print("AtChem2模拟结果摘要:")
print(f"最大O3浓度: {max_o3:.2f} ppb (在 {max_o3_time:.2f} 小时)")
print(f"平均OH浓度: {avg_oh:.2e} ppt")

# 保存结果摘要
with open('OUT/FINAL/atchem2_summary.txt', 'w') as f:
    f.write("AtChem2模拟结果摘要\n")
    f.write("="*50 + "\n")
    f.write(f"最大O3浓度: {max_o3:.2f} ppb (在 {max_o3_time:.2f} 小时)\n")
    f.write(f"平均OH浓度: {avg_oh:.2e} ppt\n")
    f.write(f"模拟时长: 24小时\n")
    f.write(f"时间步长: 5分钟\n")

print("✅ AtChem2结果分析完成")
