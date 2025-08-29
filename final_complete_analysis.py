#!/usr/bin/env python3
import subprocess
import os
import sys

def run_script(script_name, description):
    """运行单个脚本并报告结果"""
    print(f"\n{'='*50}")
    print(f"运行: {description}")
    print('='*50)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print("✓ 成功")
        if result.stdout.strip():
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"✗ 失败: {e}")
        print(e.stderr)
    except FileNotFoundError:
        print(f"✗ 未找到脚本: {script_name}")

# 步骤顺序
scripts = [
    ('optimize_data_processing.py', '数据优化处理'),
    ('fix_fonts_and_finalize.py', '最终可视化与字体修复'),
]

print("开始完整的大气化学分析...")
print("步骤:")
for i, (script, desc) in enumerate(scripts, 1):
    print(f"{i}. {desc}")

# 运行所有脚本
for script, desc in scripts:
    run_script(script, desc)

# 创建GitHub目录
if os.path.exists('AtChem2'):
    target_dir = 'AtChem2/OUT/FINAL'
else:
    target_dir = 'OUT/FINAL'

os.makedirs(target_dir, exist_ok=True)
for file in ['final_ekma_curve.png', 'final_rir_chart.png', 
             'final_time_series.png', 'final_relationships.png', 
             'ANALYSIS_REPORT.md']:
    src = f'OUT/FINAL/{file}'
    dst = f'{target_dir}/{file}'
    if os.path.exists(src):
        import shutil
        shutil.copy2(src, dst)
        print(f"复制 {file} 到 {target_dir}")

print("\n" + "="*50)
print("分析完成！")
print("="*50)
print("查看结果:")
print("OUT/FINAL/ 目录包含所有最终图表")
print("- EKMA曲线与脊线识别")
print("- RIR分析图表")
print("- 时间序列分析")
print("- 控制区域分布")
print("- 完整分析报告")
