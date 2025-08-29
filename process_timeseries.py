import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取11.csv文件
df = pd.read_csv('11.csv')
print(f"成功读取11.csv，包含 {len(df)} 行数据")
print("列名:", df.columns.tolist())

# 假设O3浓度在"茅山头O3"列，NOx相关浓度在"茅山头NO2"和"NO"列
o3_col = '茅山头O3'
nox_col = '茅山头NO2'  # 或者使用NO列
voc_cols = ['乙烯', '丙醛', '丙烯', '甲苯', '间、对-二甲苯', '丙酮']  # 根据您的数据调整

# 计算总VOC浓度
df['总VOC'] = df[voc_cols].sum(axis=1)

# 计算NOx浓度（如果NO2和NO是分开的）
if 'NO' in df.columns and nox_col in df.columns:
    df['NOx'] = df[nox_col] + df['NO']
else:
    df['NOx'] = df[nox_col]  # 或者使用其他适当的列

# 计算VOC/NOx比率
df['VOC_NOx_ratio'] = df['总VOC'] / df['NOx']

# 绘制O3与VOC/NOx比率的关系
plt.figure(figsize=(10, 6))
plt.scatter(df['VOC_NOx_ratio'], df[o3_col], alpha=0.5)
plt.xlabel('VOC/NOx Ratio')
plt.ylabel('O3 Concentration')
plt.title('O3 vs VOC/NOx Ratio')
plt.grid(True)
plt.savefig('o3_vs_voc_nox.png', dpi=300)
plt.close()

# 绘制EKMA风格的散点图
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df['总VOC'], df['NOx'], c=df[o3_col], cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='O3 Concentration')
plt.xlabel('总VOC Concentration')
plt.ylabel('NOx Concentration')
plt.title('O3 Concentration vs VOC and NOx (EKMA Style)')
plt.grid(True)
plt.savefig('ekma_style_scatter.png', dpi=300)
plt.close()

# 保存处理后的数据
df.to_csv('processed_timeseries.csv', index=False)
print("时间序列数据处理完成，结果已保存到 processed_timeseries.csv")
print("已创建图表: o3_vs_voc_nox.png 和 ekma_style_scatter.png")
