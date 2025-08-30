import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import shutil

print("进行AtChem2敏感性分析...")

# 基准情景结果
base_output = 'atchem2_output/output.csv'
if not os.path.exists(base_output):
    print("❌ 基准情景输出不存在")
    exit(1)

df_base = pd.read_csv(base_output)
base_o3_max = df_base['O3'].max()

# 创建敏感性分析目录
os.makedirs('sensitivity_analysis', exist_ok=True)

# 定义敏感性情景
scenarios = {
    'base': {'NO': 1.0, 'NO2': 1.0, 'VOC': 1.0},
    'nox_reduce_20': {'NO': 0.8, 'NO2': 0.8, 'VOC': 1.0},
    'nox_reduce_50': {'NO': 0.5, 'NO2': 0.5, 'VOC': 1.0},
    'voc_reduce_20': {'NO': 1.0, 'NO2': 1.0, 'VOC': 0.8},
    'voc_reduce_50': {'NO': 1.0, 'NO2': 1.0, 'VOC': 0.5},
}

results = {}

for scenario, factors in scenarios.items():
    print(f"运行情景: {scenario}")
    
    # 创建情景目录
    scenario_dir = f'sensitivity_analysis/{scenario}'
    os.makedirs(scenario_dir, exist_ok=True)
    
    # 修改初始浓度
    df_init = pd.read_csv('atchem2_input/initialConcentrations.config', sep='\t', comment='#', header=None)
    df_init.columns = ['time', 'species', 'value']
    
    # 应用削减因子
    for i, row in df_init.iterrows():
        species = row['species']
        if species in ['NO', 'NO2']:
            df_init.at[i, 'value'] = row['value'] * factors['NO'] if species == 'NO' else row['value'] * factors['NO2']
        elif species not in ['O3', 'CO', 'CH4', 'H2O']:  # 假设其他都是VOC
            df_init.at[i, 'value'] = row['value'] * factors['VOC']
    
    # 保存修改后的初始浓度
    with open(f'{scenario_dir}/initialConcentrations.config', 'w') as f:
        f.write("# Species initial concentrations\n")
        for _, row in df_init.iterrows():
            f.write(f"{row['time']}\t{row['species']}\t{row['value']}\n")
    
    # 复制其他配置文件
    shutil.copy('atchem2_input/environmentVariables.config', f'{scenario_dir}/')
    shutil.copy('atchem2_input/model.config', f'{scenario_dir}/')
    
    # 运行AtChem2
    cmd = [
        './build/atchem2',
        '--mechanism', 'mechanisms/mcm.csv',
        '--env-file', f'{scenario_dir}/environmentVariables.config',
        '--init-file', f'{scenario_dir}/initialConcentrations.config',
        '--config-file', f'{scenario_dir}/model.config',
        '--output-dir', f'{scenario_dir}/output'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # 读取结果
        df_scenario = pd.read_csv(f'{scenario_dir}/output/output.csv')
        max_o3 = df_scenario['O3'].max()
        results[scenario] = max_o3
        print(f"  {scenario}: 最大O3 = {max_o3:.2f} ppb")
    else:
        print(f"  {scenario}: 运行失败")
        results[scenario] = np.nan

# 计算RIR值
print("\n计算RIR值...")
rir_values = {}

# NOx的RIR
if 'nox_reduce_20' in results and 'base' in results:
    nox_rir_20 = (results['nox_reduce_20'] - results['base']) / (0.8 - 1.0) / results['base'] * 100
    rir_values['NOx_20'] = nox_rir_20

if 'nox_reduce_50' in results and 'base' in results:
    nox_rir_50 = (results['nox_reduce_50'] - results['base']) / (0.5 - 1.0) / results['base'] * 100
    rir_values['NOx_50'] = nox_rir_50

# VOC的RIR
if 'voc_reduce_20' in results and 'base' in results:
    voc_rir_20 = (results['voc_reduce_20'] - results['base']) / (0.8 - 1.0) / results['base'] * 100
    rir_values['VOC_20'] = voc_rir_20

if 'voc_reduce_50' in results and 'base' in results:
    voc_rir_50 = (results['voc_reduce_50'] - results['base']) / (0.5 - 1.0) / results['base'] * 100
    rir_values['VOC_50'] = voc_rir_50

print("RIR值:")
for k, v in rir_values.items():
    print(f"{k}: {v:.2f}%")

# 绘制RIR图表
fig, ax = plt.subplots(figsize=(10, 6))
scenarios = ['NOx_20', 'NOx_50', 'VOC_20', 'VOC_50']
values = [rir_values.get(s, 0) for s in scenarios]
colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in values]

bars = ax.bar(scenarios, values, color=colors, edgecolor='k', alpha=0.8)

for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, 
            value + 0.1 * np.sign(value), 
            f'{value:.1f}%',
            ha='center', 
            va='bottom' if value > 0 else 'top', 
            fontsize=12, fontweight='bold')

ax.axhline(0, color='k', linestyle='--', alpha=0.7)
ax.set_ylabel('Relative Incremental Reactivity (%)', fontsize=12)
ax.set_title('RIR Values from AtChem2 Sensitivity Analysis', fontsize=14)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('OUT/FINAL/atchem2_rir.png', dpi=300, bbox_inches='tight')
plt.close()

# 保存结果
with open('OUT/FINAL/atchem2_sensitivity_summary.txt', 'w') as f:
    f.write("AtChem2敏感性分析结果\n")
    f.write("="*50 + "\n")
    f.write("情景\t最大O3(ppb)\n")
    for scenario, value in results.items():
        f.write(f"{scenario}\t{value:.2f}\n")
    
    f.write("\nRIR值:\n")
    for scenario, value in rir_values.items():
        f.write(f"{scenario}\t{value:.2f}%\n")

print("✅ AtChem2敏感性分析完成")
