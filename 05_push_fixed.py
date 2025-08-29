import subprocess
import datetime
import os

# 添加所有新文件
subprocess.run(['git', 'add', '01_preprocess.py', '02_rir.py', '03_ekma.py', '04_time_rel.py', '05_push.py'], check=False)
subprocess.run(['git', 'add', 'OUT/FINAL'], check=True)

# 提交更改
try:
    subprocess.run(['git', 'commit', '-m', f'EKMA+RIR analysis results ({datetime.date.today()})'], check=True)
except subprocess.CalledProcessError:
    print("提交失败，可能没有更改需要提交")
    
# 尝试推送
try:
    subprocess.run(['git', 'push', 'origin', 'master'], check=True)
    print('✅ 推送完成')
except subprocess.CalledProcessError as e:
    print(f'推送失败: {e}')
    print('尝试强制推送...')
    subprocess.run(['git', 'push', 'origin', 'master', '--force'], check=True)
    print('✅ 强制推送完成')
