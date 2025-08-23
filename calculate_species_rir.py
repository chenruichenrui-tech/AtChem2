import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取模拟结果
try:
    df = pd.read_csv('ekma_simulation_results.csv')
    print(f"成功读取模拟结果，包含 {len(df)} 行数据")
except Exception as e:
    print(f"读取模拟结果失败: {e}")
    exit(1)

# 计算不同物种的RIR
# 这里需要根据您的化学机制定义物种类别
# 假设我们已经有了不同物种的分类信息

# 创建模拟不同物种影响的函数
def calculate_species_rir(base_conc, perturbed_conc, base_o3, perturbed_o3):
    """计算单个物种的RIR"""
    delta_conc = perturbed_conc - base_conc
    delta_o3 = perturbed_o3 - base_o3
    return delta_o3 / delta_conc if delta_conc != 0 else 0

# 假设我们已经运行了不同物种扰动的模拟
# 这里使用模拟数据来计算平均RIR

# 创建示例数据（实际应用中应使用真实模拟结果）
species_data = {
    'NOx': np.random.uniform(0.5, 2.0, 20),
    'NVOC': np.random.uniform(0.3, 1.5, 20),
    'AVOC': np.random.uniform(0.8, 3.0, 20),
    'CO': np.random.uniform(0.1, 0.5, 20)
}

# 计算平均RIR
mean_rir = {species: np.mean(values) for species, values in species_data.items()}

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(range(len(mean_rir)), list(mean_rir.values()))
plt.xlabel('Species')
plt.ylabel('Average Relative Incremental Reactivity (RIR)')
plt.title('Average RIR by Species')
plt.xticks(range(len(mean_rir)), list(mean_rir.keys()))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('species_rir_bar_chart.png', dpi=300)
plt.close()

# 保存结果
species_rir_df = pd.DataFrame.from_dict(mean_rir, orient='index', columns=['Average_RIR'])
species_rir_df.to_csv('species_rir_results.csv')
print("物种RIR计算完成，结果已保存到 species_rir_results.csv 和 species_rir_bar_chart.png")
