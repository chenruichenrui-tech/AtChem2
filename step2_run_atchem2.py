import subprocess
import os
import time

print("开始运行AtChem2模型...")

# 检查是否已编译
if not os.path.exists('build/atchem2'):
    print("编译AtChem2...")
    # 创建build目录
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    
    # 运行CMake和make
    result = subprocess.run(['cmake', '..'], capture_output=True, text=True)
    if result.returncode != 0:
        print("CMake配置失败:")
        print(result.stderr)
        exit(1)
        
    result = subprocess.run(['make'], capture_output=True, text=True)
    if result.returncode != 0:
        print("编译失败:")
        print(result.stderr)
        exit(1)
    
    os.chdir('..')
    print("✅ AtChem2编译成功")

# 运行AtChem2
print("运行AtChem2模型...")
start_time = time.time()

# 使用MCM机制运行
os.makedirs('atchem2_output', exist_ok=True)
cmd = [
    './build/atchem2',
    '--mechanism', 'mechanisms/mcm.csv',
    '--env-file', 'atchem2_input/environmentVariables.config',
    '--init-file', 'atchem2_input/initialConcentrations.config',
    '--config-file', 'atchem2_input/model.config',
    '--output-dir', 'atchem2_output'
]

result = subprocess.run(cmd, capture_output=True, text=True)

end_time = time.time()
elapsed_time = end_time - start_time

if result.returncode == 0:
    print(f"✅ AtChem2运行成功，耗时: {elapsed_time:.2f}秒")
    print("输出文件保存在 atchem2_output/ 目录")
else:
    print("❌ AtChem2运行失败:")
    print(result.stderr)
