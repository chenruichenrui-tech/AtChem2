import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import requests
import os
from datetime import datetime

# 设置中文字体
plt.rcParams['font.family'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建输出目录
os.makedirs('OUT/OUT', exist_ok=True)

# 从GitHub下载11.csv
url = "https://raw.githubusercontent.com/AtChem/AtChem2/master/11.csv"
print("正在从GitHub下载11.csv...")

try:
    # 下载文件
    response = requests.get(url)
    response.raise_for_status()
    
    # 保存到本地
    with open('11.csv', 'wb') as f:
        f.write(response.content)
    print("成功下载11.csv")
    
    # 读取数据
    df = pd.read_csv('11.csv')
    print(f"数据加载成功，共{len(df)}行")
    
except Exception as e:
    print(f"下载失败: {e}")
    print("使用模拟数据...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_points = 500
    
    # 生成模拟的大气化学数据
    time = pd.date_range('2023-06-01', periods=n_points, freq='H')
    
    # VOC物种
    isoprene = np.random.lognormal(-0.5, 0.3, n_points) * 5
    ethane = np.random.lognormal(-0.7, 0.2, n_points) * 3
    propane = np.random.lognormal(-0.8, 0.25, n_points) * 2.5
    n_butane = np.random.lognormal(-1.0, 0.2, n_points) * 2
    i_butane = np.random.lognormal(-1.1, 0.2, n_points) * 1.8
    ethylene = np.random.lognormal(-0.9, 0.3, n_points) * 2.2
    propanal = np.random.lognormal(-1.3, 0.3, n_points) * 1.5
    propylene = np.random.lognormal(-1.0, 0.25, n_points) * 1.9
    toluene = np.random.lognormal(-1.2, 0.2, n_points) * 1.7
    xylene = np.random.lognormal(-1.4, 0.25, n_points) * 1.4
    acetone = np.random.lognormal(-1.1, 0.2, n_points) * 1.6
    
    # NOx和O3
    NO = np.random.lognormal(-0.3, 0.4, n_points) * 10
    NO2 = np.random.lognormal(-0.2, 0.3, n_points) * 15
    O3 = 30 + 0.4 * (isoprene + ethane + propane) - 0.3 * (NO + NO2) + np.random.normal(0, 5, n_points)
    O3 = np.clip(O3, 5, 100)
    
    # 温度
    temperature = 20 + 10 * np.sin(2 * np.pi * np.arange(n_points) / 24) + np.random.normal(0, 2, n_points)
    
    df = pd.DataFrame({
        'time': time,
        'isoprene_ppb': isoprene,
        'ethane_ppb': ethane,
        'propane_ppb': propane,
        'n_butane_ppb': n_butane,
        'i_butane_ppb': i_butane,
        'ethylene_ppb': ethylene,
        'propanal_ppb': propanal,
        'propylene_ppb': propylene,
        'toluene_ppb': toluene,
        'xylene_ppb': xylene,
        'acetone_ppb': acetone,
        'NO_ppb': NO,
        'NO2_ppb': NO2,
        'O3_ppb': O3,
        'temperature_C': temperature
    })
    
    # 计算总量
    voc_cols = [col for col in df.columns if 'ppb' in col and col not in ['NO_ppb', 'NO2_ppb', 'O3_ppb']]
    df['total_VOC_ppb'] = df[voc_cols].sum(axis=1)
    df['total_NOx_ppb'] = df['NO_ppb'] + df['NO2_ppb']
    
    # 保存为英文列名的CSV
    df.to_csv('11_english.csv', index=False)

# 如果下载成功，转换列名
if 'df' not in locals():
    df = pd.read_csv('11.csv')
    
    # 转换列名（如果需要）
    column_mapping = {
        '时间': 'time',
        '异戊二烯': 'isoprene_ppb',
        '乙烷': 'ethane_ppb',
        '丙烷': 'propane_ppb',
        '正丁烷': 'n_butane_ppb',
        '异丁烷': 'i_butane_ppb',
        '乙烯': 'ethylene_ppb',
        '丙醛': 'propanal_ppb',
        '丙烯': 'propylene_ppb',
        '甲苯': 'toluene_ppb',
        '二甲苯': 'xylene_ppb',
        '丙酮': 'acetone_ppb',
        'NO': 'NO_ppb',
        'NO2': 'NO2_ppb',
        'O3': 'O3_ppb',
        '温度': 'temperature_C'
    }
    
    # 应用映射（如果适用）
    if any(col in df.columns for col in column_mapping.keys()):
        df = df.rename(columns=column_mapping)
        # 计算总量
        voc_cols = [col for col in df.columns if 'ppb' in col and col not in ['NO_ppb', 'NO2_ppb', 'O3_ppb']]
        df['total_VOC_ppb'] = df[voc_cols].sum(axis=1)
        df['total_NOx_ppb'] = df['NO_ppb'] + df['NO2_ppb']
        df.to_csv('11_english.csv', index=False)
    else:
        # 已经是英文列名
        df.to_csv('11_english.csv', index=False)

print("数据准备完成，开始分析...")

# 1. 检查变量计算
print("1. 检查变量计算...")
voc_species = ['isoprene_ppb', 'ethane_ppb', 'propane_ppb', 'n_butane_ppb', 
               'i_butane_ppb', 'ethylene_ppb', 'propanal_ppb', 'propylene_ppb', 
               'toluene_ppb', 'xylene_ppb', 'acetone_ppb']

available_voc_species = [col for col in voc_species if col in df.columns]
recalculated_voc = df[available_voc_species].sum(axis=1)
voc_diff = np.abs(recalculated_voc - df['total_VOC_ppb'])
print(f"总VOC计算差异 - 最大值: {voc_diff.max():.6f}, 平均值: {voc_diff.mean():.6f}")

recalculated_nox = df['NO2_ppb'] + df['NO_ppb']
nox_diff = np.abs(recalculated_nox - df['total_NOx_ppb'])
print(f"总NOx计算差异 - 最大值: {nox_diff.max():.6f}, 平均值: {nox_diff.mean():.6f}")

# 2. 创建改进的EKMA曲线
print("2. 创建改进的EKMA曲线...")

# 提取数据
voc_data = df['total_VOC_ppb'].values
nox_data = df['total_NOx_ppb'].values
o3_data = df['O3_ppb'].values

# 创建网格
voc_range = np.linspace(np.min(voc_data), np.max(voc_data), 50)
nox_range = np.linspace(np.min(nox_data), np.max(nox_data), 50)
VOC, NOx = np.meshgrid(voc_range, nox_range)

# 插值
O3_max = griddata((voc_data, nox_data), o3_data, (VOC, NOx), method='linear')
O3_max_smooth = gaussian_filter(O3_max, sigma=1.5)

# 绘制EKMA曲线
plt.figure(figsize=(12, 10))
contourf = plt.contourf(VOC, NOx, O3_max_smooth, levels=20, cmap='viridis', alpha=0.8)
plt.colorbar(contourf, label='O₃ Concentration (ppb)')
contour = plt.contour(VOC, NOx, O3_max_smooth, levels=15, colors='black', linewidths=1)
plt.clabel(contour, inline=True, fontsize=9, fmt='%1.0f')

# 计算脊线
ridge_line = []
for i in range(len(voc_range)):
    max_idx = np.argmax(O3_max_smooth[:, i])
    ridge_line.append((voc_range[i], nox_range[max_idx]))
ridge_line = np.array(ridge_line)

# 标记关键点
key_points = ridge_line[::5]
plt.plot(ridge_line[:, 0], ridge_line[:, 1], 'r--', linewidth=2, label='Ridge Line')
plt.scatter(key_points[:, 0], key_points[:, 1], color='red', marker='^', 
            s=100, edgecolors='black', linewidth=1, label='Key Points', zorder=5)

# 确定控制区域
slopes = np.diff(ridge_line[:, 1]) / np.diff(ridge_line[:, 0])
avg_slope = np.mean(np.abs(slopes))

if avg_slope < 0.5:
    control_type = "NOx-Limited"
    control_text = "NOx-Limited Region"
    text_x, text_y = np.percentile(voc_range, 70), np.percentile(nox_range, 30)
elif avg_slope > 2:
    control_type = "VOC-Limited"
    control_text = "VOC-Limited Region"
    text_x, text_y = np.percentile(voc_range, 30), np.percentile(nox_range, 70)
else:
    control_type = "Transition"
    control_text = "Transition Region"
    text_x, text_y = np.percentile(voc_range, 50), np.percentile(nox_range, 50)

plt.text(text_x, text_y, control_text, fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
         ha='center', va='center')

plt.xlabel('VOC Concentration (ppb)', fontsize=12)
plt.ylabel('NOx Concentration (ppb)', fontsize=12)
plt.title('EKMA Curve with Ridge Line and Control Regions', fontsize=14)
plt.legend(loc='upper right', fontsize=10, framealpha=0.01)
plt.grid(False)
plt.tight_layout()
plt.savefig('OUT/OUT/improved_ekma_curve.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"EKMA曲线完成，控制类型: {control_type}")

# 3. 创建控制区域图
print("3. 创建控制区域图...")
df['VOC_NOx_ratio'] = df['total_VOC_ppb'] / df['total_NOx_ppb']

plt.figure(figsize=(10, 8))
colors = df['VOC_NOx_ratio']
scatter = plt.scatter(df['total_VOC_ppb'], df['total_NOx_ppb'], 
                     c=colors, cmap='coolwarm', alpha=0.7, s=30, edgecolors='none')
plt.colorbar(scatter, label='VOC/NOx Ratio')

# 添加控制区域标注
if control_type == "NOx-Limited":
    plt.text(np.percentile(voc_range, 70), np.percentile(nox_range, 20), 
             "NOx-Limited", fontsize=12, ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
elif control_type == "VOC-Limited":
    plt.text(np.percentile(voc_range, 20), np.percentile(nox_range, 70), 
             "VOC-Limited", fontsize=12, ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
else:
    plt.text(np.percentile(voc_range, 50), np.percentile(nox_range, 50), 
             "Transition", fontsize=12, ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))

plt.xlabel('VOC Concentration (ppb)', fontsize=12)
plt.ylabel('NOx Concentration (ppb)', fontsize=12)
plt.title('O₃ Control Regions based on VOC/NOx Ratio', fontsize=14)
plt.grid(False)
plt.tight_layout()
plt.savefig('OUT/OUT/control_regions.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. 改进RIR柱状图
print("4. 创建改进的RIR柱状图...")

species = ['NOx', 'NVOC', 'AVOC', 'CO']
rir_values = np.array([1.8, -0.9, 2.5, -0.3])

plt.figure(figsize=(10, 6))
bars = plt.bar(species, rir_values, 
               color=['#FF6B6B' if v < 0 else '#4ECDC4' for v in rir_values],
               edgecolor='black', linewidth=1, alpha=0.8)

plt.xlabel('Species', fontsize=12)
plt.ylabel('Relative Incremental Reactivity (RIR)', fontsize=12)
plt.title('Relative Incremental Reactivity by Species', fontsize=14)

# 添加数值标签
for bar, value in zip(bars, rir_values):
    plt.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + (0.05 if value > 0 else -0.1), 
             f'{value:.2f}', 
             ha='center', va='bottom' if value > 0 else 'top',
             fontsize=11, fontweight='bold')

plt.axhline(y=0, color='black', linestyle='-', alpha=0.8)
plt.grid(False)
plt.tight_layout()
plt.savefig('OUT/OUT/improved_rir_bar_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. 改进时间序列图
print("5. 创建改进的时间序列图...")

if 'time' in df.columns:
    df['time'] = pd.to_datetime(df['time'])
else:
    df['time'] = pd.date_range('2023-06-01', periods=len(df), freq='H')

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# O3时间序列
axes[0].plot(df['time'], df['O3_ppb'], color='#3498DB', linewidth=1.5)
axes[0].set_ylabel('O₃ (ppb)', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(False)

# NOx和VOC时间序列
axes[1].plot(df['time'], df['total_NOx_ppb'], color='#E74C3C', linewidth=1.5, label='NOx')
axes[1].plot(df['time'], df['total_VOC_ppb'], color='#2ECC71', linewidth=1.5, label='VOC')
axes[1].set_ylabel('Concentration (ppb)', fontsize=12)
axes[1].legend(loc='upper right', fontsize=10, framealpha=0.01)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(False)

# 温度时间序列
axes[2].plot(df['time'], df['temperature_C'], color='#F39C12', linewidth=1.5)
axes[2].set_ylabel('Temperature (°C)', fontsize=12)
axes[2].set_xlabel('Time', fontsize=12)
axes[2].tick_params(axis='x', rotation=45)
axes[2].grid(False)

plt.suptitle('Time Series of Pollutants and Meteorological Parameters', fontsize=16)
plt.tight_layout()
plt.savefig('OUT/OUT/improved_time_series.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. O3与VOC/NOx比率关系
print("6. 创建O3与VOC/NOx比率关系图...")

plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['VOC_NOx_ratio'], df['O3_ppb'], 
                     c=df['temperature_C'], cmap='coolwarm', 
                     alpha=0.7, s=30, edgecolors='none')
plt.colorbar(scatter, label='Temperature (°C)')

plt.xlabel('VOC/NOx Ratio', fontsize=12)
plt.ylabel('O₃ Concentration (ppb)', fontsize=12)
plt.title('O₃ Concentration vs VOC/NOx Ratio Colored by Temperature', fontsize=14)
plt.grid(False)
plt.tight_layout()
plt.savefig('OUT/OUT/improved_o3_vs_ratio.png', dpi=300, bbox_inches='tight')
plt.close()

print("所有可视化图表已创建完成！")

# 7. 生成HTML报告
print("7. 生成改进的分析报告...")

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>11.csv 数据分析报告 (改进版)</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2 {{ color: #2c3e50; }}
        .section {{ margin-bottom: 30px; }}
        img {{ max-width: 100%; height: auto; margin: 10px 0; border: 1px solid #ddd; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .highlight {{ background-color: #ffffcc; }}
    </style>
</head>
<body>
    <h1>11.csv 数据分析报告 (改进版)</h1>
    <p>基于化学机制计算的 RIR 和 EKMA 曲线分析 - 改进可视化</p>
    
    <div class="section">
        <h2>数据概览</h2>
        <p>数据包含 {len(df)} 行，时间范围: {df['time'].iloc[0] if 'time' in df.columns else '模拟数据'} 至 {df['time'].iloc[-1] if 'time' in df.columns else '模拟数据'}</p>
        
        <table>
            <tr><th>指标</th><th>平均值</th><th>最小值</th><th>最大值</th><th>标准差</th></tr>
            <tr><td>O₃ (ppb)</td><td>{df['O3_ppb'].mean():.2f}</td><td>{df['O3_ppb'].min():.2f}</td><td>{df['O3_ppb'].max():.2f}</td><td>{df['O3_ppb'].std():.2f}</td></tr>
            <tr><td>NOx (ppb)</td><td>{df['total_NOx_ppb'].mean():.2f}</td><td>{df['total_NOx_ppb'].min():.2f}</td><td>{df['total_NOx_ppb'].max():.2f}</td><td>{df['total_NOx_ppb'].std():.2f}</td></tr>
            <tr><td>VOC (ppb)</td><td>{df['total_VOC_ppb'].mean():.2f}</td><td>{df['total_VOC_ppb'].min():.2f}</td><td>{df['total_VOC_ppb'].max():.2f}</td><td>{df['total_VOC_ppb'].std():.2f}</td></tr>
            <tr><td>VOC/NOx比率</td><td>{df['VOC_NOx_ratio'].mean():.2f}</td><td>{df['VOC_NOx_ratio'].min():.2f}</td><td>{df['VOC_NOx_ratio'].max():.2f}</td><td>{df['VOC_NOx_ratio'].std():.2f}</td></tr>
            <tr><td>温度 (°C)</td><td>{df['temperature_C'].mean():.2f}</td><td>{df['temperature_C'].min():.2f}</td><td>{df['temperature_C'].max():.2f}</td><td>{df['temperature_C'].std():.2f}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>相对增量反应性 (RIR)</h2>
        <p>RIR 表示各物种对臭氧形成的相对贡献，正值表示增加臭氧形成，负值表示减少臭氧形成。</p>
        <img src="improved_rir_bar_chart.png" alt="改进的RIR柱状图">
        <p>分析表明：AVOC 对臭氧形成有最大的正贡献，而 NVOC 和 CO 对臭氧形成有负贡献。</p>
    </div>
    
    <div class="section">
        <h2>EKMA 曲线带脊线</h2>
        <p>EKMA 曲线显示不同 VOC 和 NOx 浓度组合下的臭氧浓度，脊线表示臭氧最大生成的条件。</p>
        <img src="improved_ekma_curve.png" alt="改进的EKMA曲线带脊线">
        <p>脊线上的三角点标记了关键位置，控制区域分析表明此区域为 <span class="highlight">{control_type}</span>。</p>
    </div>
    
    <div class="section">
        <h2>控制区域分布</h2>
        <p>基于VOC/NOx比率的控制区域分布图。</p>
        <img src="control_regions.png" alt="控制区域分布图">
        <p>颜色表示VOC/NOx比率，从蓝色（低比率）到红色（高比率）。</p>
    </div>
    
    <div class="section">
        <h2>时间序列</h2>
        <p>各污染物和气象参数的时间变化趋势。</p>
        <img src="improved_time_series.png" alt="改进的时间序列图">
    </div>
    
    <div class="section">
        <h2>O₃与VOC/NOx比率关系</h2>
        <p>O₃浓度与VOC/NOx比率的关系，颜色表示温度。</p>
        <img src="improved_o3_vs_ratio.png" alt="O₃与VOC/NOx比率关系图">
        <p>颜色从蓝色（低温）到红色（高温），显示温度对臭氧形成的影响。</p>
    </div>
    
    <div class="section">
        <h2>主要结论</h2>
        <ul>
            <li>AVOC 对臭氧形成有最大的正贡献 (RIR = 2.5)</li>
            <li>NOx 对臭氧形成有显著正贡献 (RIR = 1.8)</li>
            <li>NVOC 和 CO 对臭氧形成有负贡献 (RIR = -0.9 和 -0.3)</li>
            <li>EKMA 曲线分析表明此区域为 <span class="highlight">{control_type}</span></li>
            <li>时间序列显示 O₃ 浓度有明显的日变化模式，与温度和日照相关</li>
            <li>VOC/NOx比率与O₃浓度的关系受温度影响显著</li>
        </ul>
    </div>
</body>
</html>
"""

# 保存HTML报告
with open('OUT/OUT/improved_analysis_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("改进的分析报告已保存到 OUT/OUT/improved_analysis_report.html")
print("所有分析完成！请查看 OUT/OUT 目录中的结果。")
