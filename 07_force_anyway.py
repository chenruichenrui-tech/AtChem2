import subprocess, datetime, os

# 1. 强制提交
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', f'EKMA+RIR 11.csv ({datetime.date.today()})', '--allow-empty'], check=True)

# 2. 强制推送（覆盖远程）
subprocess.run(['git', 'push', 'origin', 'master', '--force'], check=True)

print('✅ 强制推送成功！')
