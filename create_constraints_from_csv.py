import csv
import pathlib

csvfile = '11.csv'
constraints_dir = pathlib.Path('model/constraints/species')

# 确保约束目录存在
constraints_dir.mkdir(parents=True, exist_ok=True)

# 映射关系：AtChem2物种名 -> CSV列名
species_mapping = {
    'NO': 'NO',
    'NO2': '茅山头NO2',
    'O3': '茅山头O3',
    'CO': '茅山头CO',
    'SO2': '茅山头SO2',
    'HCHO': 'CH₂O',
    'CH4': 'CH4',
    'ISOP': '异戊二烯',
    'C2H6': '乙烷',
    'C3H8': '丙烷',
    'NC4H10': '正丁烷',
    'IC4H10': '异丁烷',
    'C2H4': '乙烯',
    'C3H6': '丙烯',
    'TOLUENE': '甲苯',
    'MXYL': '间、对-二甲苯',
    'ACETONE': '丙酮'
}

# 观测值 → molec cm-3 的换算系数（25 °C, 1 atm）
ppb2molec = 2.46e10

# 读取CSV文件
with open(csvfile, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 为每个约束物种创建时间序列文件
constrained_species = []
with open('model/configuration/speciesConstrained.config', 'r') as f:
    for line in f:
        if line.strip():
            species = line.split()[0]
            constrained_species.append(species)

for species in constrained_species:
    csv_column = species_mapping.get(species, species)
    
    with open(constraints_dir / species, 'w') as f:
        for i, row in enumerate(rows):
            if csv_column in row and row[csv_column].strip():
                try:
                    # 将CSV中的值转换为分子浓度
                    val = float(row[csv_column]) * ppb2molec
                    # 时间（秒），假设每小时一个数据点
                    time_sec = i * 3600
                    f.write(f"{time_sec} {val:.5e}\n")
                except ValueError:
                    print(f"警告: 无法转换 {csv_column} 的值: {row[csv_column]}")
            else:
                print(f"警告: 未找到列 {csv_column} 或值为空，使用默认值")
                # 使用speciesConstrained.config中的默认值
                default_val = None
                with open('model/configuration/speciesConstrained.config', 'r') as cfg:
                    for cfg_line in cfg:
                        if cfg_line.startswith(species):
                            default_val = cfg_line.split()[1]
                            break
                
                if default_val:
                    time_sec = i * 3600
                    f.write(f"{time_sec} {default_val}\n")

print("约束文件创建完成!")
