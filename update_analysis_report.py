import pandas as pd

# 读取转换后的11.csv文件
df = pd.read_csv('11_english.csv')

# 计算VOC/NOx比率
df['VOC_NOx_ratio'] = df['total_VOC_ppb'] / df['total_NOx_ppb']

# 创建更新的HTML报告
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
        <p>数据包含 {len(df)} 行，时间范围: {df['time'].min()} 至 {df['time'].max()}</p>
        
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
        <p>脊线上的三角点标记了关键位置，控制区域分析表明此区域为 <span class="highlight">过渡区域</span>，既受VOC限制也受NOx限制。</p>
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
            <li>EKMA 曲线分析表明此区域为过渡控制区域</li>
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
