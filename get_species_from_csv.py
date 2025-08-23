import csv

csvfile = '11.csv'
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

# 读取CSV文件的第一行获取表头
with open(csvfile, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print("CSV文件中的列:", headers)

# 找出哪些物种在CSV中有数据
available_species = []
for chem_species, csv_column in species_mapping.items():
    if csv_column in headers:
        available_species.append(chem_species)

print("CSV中可用的物种:", available_species)
