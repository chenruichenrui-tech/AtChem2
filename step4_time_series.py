import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置字体
plt.rcParams['font.family'] = 'DejaVu Sans'

# 读取处理后的数据
df = pd.read_csv('OUT/11_processed.csv')
df['time'] = pd.to_datetime(df['time'])

# 绘制时间序列图
fig, axes = plt.subplots(4, 1, figsize=(15, 10), sharex=True)
for ax, col, lab in zip(axes, ['O3_ppb', 'total_NOx_ppb', 'total_VOC_ppb', 'temperature_C'], 
                        ['O3 (ppb)', 'NOx (ppb)', 'VOC (ppb)', 'Temperature (C)']):
    ax.plot(df['time'], df[col])
    ax.set_ylabel(lab)
    ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('OUT/FINAL/time_series.png')
plt.close()

# 绘制关系图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# VOC vs NOx
scatter = ax1.scatter(df['total_VOC_ppb'], df['total_NOx_ppb'], c=df['O3_ppb'], cmap='plasma', s=30)
plt.colorbar(scatter, ax=ax1, label='O3 (ppb)')
ax1.set_xlabel('VOC (ppb)')
ax1.set_ylabel('NOx (ppb)')
ax1.set_title('VOC vs NOx (color indicates O3 concentration)')
ax1.grid(True, alpha=0.3)

# O3 vs VOC/NOx比率
ax2.scatter(df['total_VOC_ppb']/df['total_NOx_ppb'], df['O3_ppb'], s=30)
ax2.set_xlabel('VOC/NOx Ratio')
ax2.set_ylabel('O3 (ppb)')
ax2.set_title('O3 vs VOC/NOx Ratio')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('OUT/FINAL/relationships.png')
plt.close()

print("✅ 步骤4完成: 时间序列和关系图绘制")
