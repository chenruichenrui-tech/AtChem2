import subprocess, datetime, os

# 1. 强制添加所有新文件
subprocess.run(['git', 'add', 'OUT/FINAL'], check=True)

# 2. 提交（即使无改动也强制提交）
subprocess.run(['git', 'commit', '-m', f'Add EKMA+RIR from 11.csv ({datetime.date.today()})'], check=True)

# 3. 拉取并强制推送
subprocess.run(['git', 'pull', '--rebase', 'origin', 'master'], check=True)
subprocess.run(['git', 'push', 'origin', 'master'], check=True)
print('✅ 推送完成')
