import subprocess
import os

print("检查AtChem2环境...")

# 检查AtChem2目录结构
required_dirs = ['model', 'mechanisms', 'build', 'output']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"✅ 目录存在: {dir_name}")
    else:
        print(f"❌ 目录缺失: {dir_name}")

# 检查是否已编译
if os.path.exists('build/atchem2'):
    print("✅ AtChem2已编译")
else:
    print("❌ AtChem2未编译，需要先编译")

# 检查示例机制文件
mechanism_files = ['mechanisms/mcm.csv', 'mechanisms/standard.csv']
for mech_file in mechanism_files:
    if os.path.exists(mech_file):
        print(f"✅ 机制文件存在: {mech_file}")
    else:
        print(f"❌ 机制文件缺失: {mech_file}")

print("\n环境检查完成")
