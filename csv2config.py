import csv, pathlib

# 输入输出文件
csvfile = '10.csv'
out_dir = pathlib.Path('model/configuration')

# 观测值 → molec cm-3 的换算系数（25 °C, 1 atm）
ppb2molec = 2.46e10

# 映射关系：AtChem2物种名 -> CSV列名
species_mapping = {
    'NO': 'NO',
    'NO2': '茅山头NO2',
    'O3': '茅山头O3',
    'CO': '茅山头CO',
    'SO2': '茅山头SO2',
    'HCHO': 'CH₂O',
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

# 读取CSV文件
with open(csvfile, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    row = next(reader)  # 读取第一行数据 (0:00)

# 创建物种浓度配置
constant_content = ""
constrained_content = "CH4 4.0e13\n"  # 约束物种配置

for chem_species, csv_column in species_mapping.items():
    if csv_column in row and row[csv_column].strip():
        try:
            # 将CSV中的值转换为分子浓度
            val = float(row[csv_column]) * ppb2molec
            constant_content += f"{chem_species} {val:.5e}\n"
        except ValueError:
            print(f"警告: 无法转换 {csv_column} 的值: {row[csv_column]}")
    else:
        print(f"警告: 未找到列 {csv_column} 或值为空")

# 写入配置文件
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / 'speciesConstant.config').write_text(constant_content)
(out_dir / 'speciesConstrained.config').write_text(constrained_content)

print("配置文件生成完成!")
