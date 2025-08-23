import pandas as pd
import numpy as np
import subprocess
import os
import shutil

# 设置 VOC 和 NOx 浓度范围（根据您的数据范围调整）
voc_range = np.linspace(1e10, 1e13, 10)  # VOC 浓度范围
nox_range = np.linspace(1e9, 1e12, 10)   # NOx 浓度范围

# 创建结果目录
os.makedirs('ekma_simulations', exist_ok=True)

# 备份原始配置文件
shutil.copy('model/configuration/initialConcentrations.config', 
            'model/configuration/initialConcentrations.config.backup')

results = []

# 运行批量模拟
for i, voc_conc in enumerate(voc_range):
    for j, nox_conc in enumerate(nox_range):
        print(f"运行模拟 ({i+1}/{len(voc_range)}, {j+1}/{len(nox_range)}): VOC={voc_conc:.2e}, NOx={nox_conc:.2e}")
        
        # 创建新的初始浓度配置文件
        with open('model/configuration/initialConcentrations.config', 'w') as f:
            # 添加VOC和NOx浓度
            f.write(f"VOC {voc_conc}\n")
            f.write(f"NOX {nox_conc}\n")
            # 添加其他物种的初始浓度（从备份文件中提取）
            with open('model/configuration/initialConcentrations.config.backup', 'r') as backup:
                for line in backup:
                    if not line.startswith(('VOC', 'NOX')):
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
            
            print(f"完成模拟: O3_max={o3_max:.2e}")
        else:
            print(f"模拟失败: {result.stderr}")

# 恢复原始配置文件
shutil.copy('model/configuration/initialConcentrations.config.backup', 
            'model/configuration/initialConcentrations.config')

# 保存结果到CSV文件
results_df = pd.DataFrame(results)
results_df.to_csv('ekma_simulation_results.csv', index=False)
print("所有模拟完成，结果已保存到 ekma_simulation_results.csv")
