import pandas as pd
import numpy as np

# 读取转换后的11.csv文件
df = pd.read_csv('11_english.csv')
print("检查变量计算正确性...")

# 检查总VOC计算
voc_species = ['isoprene_ppb', 'ethane_ppb', 'propane_ppb', 'n_butane_ppb', 
               'i_butane_ppb', 'ethylene_ppb', 'propanal_ppb', 'propylene_ppb', 
               'toluene_ppb', 'xylene_ppb', 'acetone_ppb']

# 确保所有VOC物种都存在
available_voc_species = [col for col in voc_species if col in df.columns]
print(f"可用的VOC物种: {available_voc_species}")

# 重新计算总VOC
recalculated_voc = df[available_voc_species].sum(axis=1)

# 比较重新计算的值与原始值
voc_diff = np.abs(recalculated_voc - df['total_VOC_ppb'])
print(f"总VOC计算差异 - 最大值: {voc_diff.max():.6f}, 平均值: {voc_diff.mean():.6f}")

# 检查总NOx计算
if 'NO2_ppb' in df.columns and 'NO_ppb' in df.columns:
    recalculated_nox = df['NO2_ppb'] + df['NO_ppb']
    nox_diff = np.abs(recalculated_nox - df['total_NOx_ppb'])
    print(f"总NOx计算差异 - 最大值: {nox_diff.max():.6f}, 平均值: {nox_diff.mean():.6f}")
else:
    print("无法检查总NOx计算，缺少NO2或NO列")

# 检查数据范围
print("\n数据范围检查:")
print(f"O3范围: {df['O3_ppb'].min():.2f} - {df['O3_ppb'].max():.2f} ppb")
print(f"VOC范围: {df['total_VOC_ppb'].min():.2f} - {df['total_VOC_ppb'].max():.2f} ppb")
print(f"NOx范围: {df['total_NOx_ppb'].min():.2f} - {df['total_NOx_ppb'].max():.2f} ppb")

# 检查VOC/NOx比率
df['VOC_NOx_ratio'] = df['total_VOC_ppb'] / df['total_NOx_ppb']
print(f"VOC/NOx比率范围: {df['VOC_NOx_ratio'].min():.2f} - {df['VOC_NOx_ratio'].max():.2f}")

# 检查异常值
print("\n异常值检查:")
for col in ['O3_ppb', 'total_VOC_ppb', 'total_NOx_ppb']:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    print(f"{col} 异常值数量: {len(outliers)}")

print("\n变量检查完成!")
