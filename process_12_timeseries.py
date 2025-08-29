import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取12.csv文件
df = pd.read_csv('12.csv')
print(f"成功读取12.csv，包含 {len(df)} 行数据")
print("列名:", df.columns.tolist())

# 计算VOC/NOx比率
df['VOC_NOx_ratio'] = df['VOC_ppb'] / df['NOx_ppb']

# 绘制O3与VOC/NOx比率的关系
plt.figure(figsize=(10, 6))
plt.scatter(df['VOC_NOx_ratio'], df['O3_ppb'], alpha=0.5)
plt.xlabel('VOC/NOx Ratio')
plt.ylabel('O3 Concentration (ppb)')
plt.title('O3 vs VOC/NOx Ratio')
plt.grid(True)
plt.savefig('OUT/12_o3_vs_voc_nox.png', dpi=300)
plt.close()

# 绘制时间序列
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# O3时间序列
axes[0].plot(df['时间'], df['O3_ppb'], color='blue')
axes[0].set_title('O3 Concentration Time Series')
axes[0].set_ylabel('O3 (ppb)')
axes[0].tick_params(axis='x', rotation=45)

# NOx和VOC时间序列
axes[1].plot(df['时间'], df['NOx_ppb'], color='red', label='NOx')
axes[1].plot(df['时间'], df['VOC_ppb'], color='green', label='VOC')
axes[1].set_title('NOx and VOC Concentration Time Series')
axes[1].set_ylabel('Concentration (ppb)')
axes[1].legend()
axes[1].tick_params(axis='x', rotation=45)

# 温度和时间序列
axes[2].plot(df['时间'], df['温度_℃'], color='orange')
axes[2].set_title('Temperature Time Series')
axes[2].set_ylabel('Temperature (°C)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('OUT/12_time_series.png', dpi=300)
plt.close()

# 绘制EKMA风格的散点图
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df['VOC_ppb'], df['NOx_ppb'], c=df['O3_ppb'], cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='O3 Concentration (ppb)')
plt.xlabel('VOC Concentration (ppb)')
plt.ylabel('NOx Concentration (ppb)')
plt.title('O3 Concentration vs VOC and NOx (EKMA Style)')
plt.grid(True)
plt.savefig('OUT/12_ekma_style_scatter.png', dpi=300)
plt.close()

# 保存处理后的数据
df.to_csv('OUT/12_processed_timeseries.csv', index=False)
print("时间序列数据处理完成，结果已保存到 OUT/12_processed_timeseries.csv")
print("已创建图表: OUT/12_o3_vs_voc_nox.png, OUT/12_time_series.png, OUT/12_ekma_style_scatter.png")
