import subprocess, datetime, os

# 1. 强制提交所有文件（包括未跟踪）
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', f'EKMA+RIR 11.csv ({datetime.date.today()})', '--allow-empty'], check=True)

# 2. 强制推送（跳过 rebase）
subprocess.run(['git', 'push', 'origin', 'master'], check=True)

print('✅ 强制推送完成！')
