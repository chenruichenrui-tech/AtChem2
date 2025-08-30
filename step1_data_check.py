import pandas as pd
import numpy as np

# 读取原始数据
df = pd.read_csv('11.csv')
print("原始数据前3行:")
print(df.head(3))
print("\n原始数据列名:")
print(df.columns.tolist())
print("\n原始数据基本信息:")
print(df.info())
print("\n原始数据缺失值统计:")
print(df.isnull().sum())

# 定义列名映射
mapping = {
    '时间': 'time',
    '茅山头O3': 'O3_ppb', 
    '茅山头CO': 'CO_ppb',
    '茅山头NO2': 'NO2_ppb',
    'NO': 'NO_ppb',
    '2m温度℃': 'temperature_C',
    '紫外线辐射J/m²': 'UV_radiation',
    '气压pa': 'pressure_pa',
    '相对湿度%': 'humidity_percent',
    '边界层高度m': 'boundary_layer_height_m',
    '风速m/s': 'wind_speed_mps',
    '茅山头PM2.5': 'PM25_ugm3',
    '茅山头SO2': 'SO2_ppb',
    'CH₂O': 'CH2O_ppb',
    'CH4': 'CH4_ppb',
    '异戊二烯': 'isoprene_ppb',
    '乙烷': 'ethane_ppb',
    '丙烷': 'propane_ppb',
    '正丁烷': 'n_butane_ppb',
    '异丁烷': 'i_butane_ppb',
    '乙烯': 'ethylene_ppb',
    '丙醛': 'propanal_ppb',
    '丙烯': 'propylene_ppb',
    '甲苯': 'toluene_ppb',
    '间、对-二甲苯': 'xylene_ppb',
    '丙酮': 'acetone_ppb'
}

# 重命名列
df = df.rename(columns=mapping)

# 识别VOC列
voc_cols = [c for c in df.columns if '_ppb' in c and c not in ['O3_ppb', 'NO2_ppb', 'NO_ppb', 'CO_ppb', 'SO2_ppb', 'CH2O_ppb', 'CH4_ppb']]
print(f"\n识别出的VOC列: {voc_cols}")

# 计算总VOC和总NOx
df['total_VOC_ppb'] = df[voc_cols].sum(axis=1)
df['total_NOx_ppb'] = df['NO_ppb'] + df['NO2_ppb']

# 保存处理后的数据
import os
os.makedirs('OUT', exist_ok=True)
df.to_csv('OUT/11_processed.csv', index=False)

print("\n处理后的数据前3行:")
print(df[['time', 'O3_ppb', 'total_VOC_ppb', 'total_NOx_ppb']].head(3))
print("\n✅ 步骤1完成: 数据检查和预处理")
