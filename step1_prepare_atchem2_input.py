import pandas as pd
import numpy as np
import os

# 读取处理后的数据
df = pd.read_csv('OUT/11_processed.csv')

# 计算平均值作为初始条件
initial_conditions = {
    'O3': df['O3_ppb'].mean(),
    'NO': df['NO_ppb'].mean(),
    'NO2': df['NO2_ppb'].mean(),
    'CO': df['CO_ppb'].mean(),
    'CH4': df['CH4_ppb'].mean() if 'CH4_ppb' in df.columns else 1800,  # 默认值
    'H2O': 1.5e4,  # 水汽浓度，根据相对湿度估算
    'TEMP': df['temperature_C'].mean() + 273.15,  # 转换为开尔文
    'PRES': df['pressure_pa'].mean() if 'pressure_pa' in df.columns else 101325  # 默认值
}

# 添加VOC物种
voc_species = ['isoprene_ppb', 'ethane_ppb', 'propane_ppb', 'n_butane_ppb', 
               'i_butane_ppb', 'ethylene_ppb', 'propanal_ppb', 'propylene_ppb', 
               'toluene_ppb', 'xylene_ppb', 'acetone_ppb']

for species in voc_species:
    if species in df.columns:
        initial_conditions[species.upper().replace('_PPB', '')] = df[species].mean()

# 创建AtChem2环境配置文件
env_config = """# Environment variables configuration
# Time (s)	Variable	Value
0	TEMP	{temp}
0	PRES	{pres}
0	H2O	{h2o}
0	JDAY	180
0	LAT	30.0
0	LON	120.0
""".format(
    temp=initial_conditions['TEMP'],
    pres=initial_conditions['PRES'],
    h2o=initial_conditions['H2O']
)

# 创建AtChem2初始浓度配置文件
species_config = "# Species initial concentrations\n"
for species, value in initial_conditions.items():
    if species not in ['TEMP', 'PRES', 'H2O', 'JDAY', 'LAT', 'LON']:
        species_config += f"0\t{species}\t{value}\n"

# 保存配置文件
os.makedirs('atchem2_input', exist_ok=True)
with open('atchem2_input/environmentVariables.config', 'w') as f:
    f.write(env_config)

with open('atchem2_input/initialConcentrations.config', 'w') as f:
    f.write(species_config)

# 创建模型配置
model_config = """# Model configuration
model.time.start = 0
model.time.end = 86400  # 24小时模拟
model.time.step = 300   # 5分钟输出间隔

model.photolysis.adjust = true

output.frequency = 300
output.species = O3, NO, NO2, OH, HO2, RO2
output.species.all = false

solver.type = rosenbrock
solver.absolute.tolerance = 1.0e-6
solver.relative.tolerance = 1.0e-4
"""

with open('atchem2_input/model.config', 'w') as f:
    f.write(model_config)

print("✅ AtChem2输入文件准备完成")
print(f"初始条件已保存到 atchem2_input/ 目录")
