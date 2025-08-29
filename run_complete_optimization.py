#!/bin/bash
echo "开始优化的大气化学数据分析..."

# 运行各个优化脚本
echo "1. 优化数据处理..."
python3 optimize_data_processing.py

echo "2. 优化EKMA分析..."
python3 optimized_ekma_analysis.py

echo "3. 综合可视化..."
python3 comprehensive_visualization.py

# 复制结果到GitHub目录
cp -r OUT/ AtChem2/ 2>/dev/null || cp -r OUT/ ./AtChem2/

echo "优化完成！结果已保存到 OUT/OUT/ 目录"
echo "主要文件："
echo "- optimized_ekma_curve.png: 优化的EKMA曲线"
echo "- enhanced_rir_chart.png: 改进的RIR图表"
echo "- enhanced_time_series.png: 时间序列图"
echo "- control_regions_distribution.png: 控制区域分布"
