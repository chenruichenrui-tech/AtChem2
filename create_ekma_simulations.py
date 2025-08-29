import pandas as pd
import subprocess
import os
import shutil

# 读取11.csv文件
try:
    df = pd.read_csv('11.csv')
    print(f"成功读取11.csv，包含 {len(df)} 行数据")
    print(df.head())
except Exception as e:
    print(f"读取11.csv失败: {e}")
    exit(1)

# 创建结果目录
os.makedirs('ekma_results', exist_ok=True)

# 备份原始配置文件
shutil.copy('model/configuration/initialConcentrations.config', 
            'model/configuration/initialConcentrations.config.backup')

results = []

for index, row in df.iterrows():
    # 假设CSV文件有两列：VOC_conc和NOx_conc
    # 如果列名不同，请根据实际情况调整
    voc_conc = row['VOC_conc'] if 'VOC_conc' in row else row[0]
    nox_conc = row['NOx_conc'] if 'NOx_conc' in row else row[1]
    
    print(f"运行 {index+1}/{len(df)}: VOC={voc_conc}, NOx={nox_conc}")
    
    # 创建新的初始浓度配置文件
    with open('model/configuration/initialConcentrations.config', 'w') as f:
        # 添加VOC和NOx浓度
        f.write(f"VOC {voc_conc}\n")
        f.write(f"NOx {nox_conc}\n")
        # 添加其他物种的初始浓度（从备份文件中提取）
        with open('model/configuration/initialConcentrations.config.backup', 'r') as backup:
            for line in backup:
                if not line.startswith(('VOC', 'NOx')):
                    f.write(line)
    
    # 运行AtChem2
    result = subprocess.run(['./atchem2'], capture_output=True, text=True)
    
    if result.returncode == 0:
        # 读取O3最大浓度
        try:
            with open('model/output/speciesConcentrations.output', 'r') as f:
                lines = f.readlines()
                # 跳过标题行
                data_lines = lines[1:]
                o3_max = 0
                for line in data_lines:
                    parts = line.split()
                    if len(parts) > 3:  # O3在第4列
                        try:
                            o3_conc = float(parts[3])
                            if o3_conc > o3_max:
                                o3_max = o3_conc
                        except ValueError:
                            continue
        except Exception as e:
            print(f"读取输出文件失败: {e}")
            o3_max = 0
        
        # 保存结果
        results.append({
            'VOC_conc': voc_conc,
            'NOx_conc': nox_conc,
            'O3_max': o3_max
        })
        
        # 复制输出文件到结果目录
        run_dir = f'ekma_results/run_{index}'
        os.makedirs(run_dir, exist_ok=True)
        
        # 复制所有输出文件
        for file in os.listdir('model/output'):
            if file != 'reactionRates':  # 跳过目录
                shutil.copy(f'model/output/{file}', f'{run_dir}/{file}')
        
        print(f"完成运行 {index+1}/{len(df)}: O3_max={o3_max}")
    else:
        print(f"运行 {index+1} 失败: {result.stderr}")

# 恢复原始配置文件
shutil.copy('model/configuration/initialConcentrations.config.backup', 
            'model/configuration/initialConcentrations.config')

# 保存结果到CSV文件
results_df = pd.DataFrame(results)
results_df.to_csv('ekma_results.csv', index=False)
print("所有运行完成，结果已保存到 ekma_results.csv")
