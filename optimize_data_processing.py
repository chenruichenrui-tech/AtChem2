import pandas as pd
import numpy as np

# 读取原始数据
print("读取原始数据...")
try:
    df = pd.read_csv('11.csv')
    print("成功读取11.csv")
except FileNotFoundError:
    print("11.csv未找到，尝试11_english.csv")
    df = pd.read_csv('11_english.csv')

print(f"数据形状: {df.shape}")
print("原始列名:", df.columns.tolist())

# 创建优化的列名映射
column_mapping = {
    '时间': 'time',
    '茅山头O3': 'O3_ppb',
    '茅山头CO': 'CO_ppb',
    '茅山头NO2': 'NO2_ppb',
    'NO': 'NO_ppb',
    '2m温度℃': 'temperature_C',
    '紫外线辐射J/m²': 'UV_radiation',
    '气压pa': 'pressure_Pa',
    '相对湿度%': 'relative_humidity',
    '边界层高度m': 'boundary_layer_height',
    '风速m/s': 'wind_speed',
    '茅山头PM2.5': 'PM2.5_ug_m3',
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

# 应用列名转换
df = df.rename(columns=column_mapping)

# 检查并计算总量
voc_cols = ['isoprene_ppb', 'ethane_ppb', 'propane_ppb', 'n_butane_ppb', 
            'i_butane_ppb', 'ethylene_ppb', 'propanal_ppb', 'propylene_ppb',
            'toluene_ppb', 'xylene_ppb', 'acetone_ppb']

# 确保所有VOC列存在
existing_voc_cols = [col for col in voc_cols if col in df.columns]
print(f"存在的VOC列: {existing_voc_cols}")

# 计算总量
df['total_VOC_ppb'] = df[existing_voc_cols].sum(axis=1)
df['total_NOx_ppb'] = df['NO2_ppb'] + df['NO_ppb']

# 转换时间格式
df['time'] = pd.to_datetime(df['time'])

# 计算VOC/NOx比率
df['VOC_NOx_ratio'] = df['total_VOC_ppb'] / df['total_NOx_ppb']

# 保存处理后的数据
df.to_csv('11_processed.csv', index=False)
print("数据处理完成，保存为11_processed.csv")

# 数据验证
print("\n数据验证:")
print(f"VOC总量范围: {df['total_VOC_ppb'].min():.2f} - {df['total_VOC_ppb'].max():.2f} ppb")
print(f"NOx总量范围: {df['total_NOx_ppb'].min():.2f} - {df['total_NOx_ppb'].max():.2f} ppb")
print(f"O3范围: {df['O3_ppb'].min():.2f} - {df['O3_ppb'].max():.2f} ppb")
print(f"VOC/NOx比率: {df['VOC_NOx_ratio'].min():.2f} - {df['VOC_NOx_ratio'].max():.2f}")
