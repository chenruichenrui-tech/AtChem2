import subprocess, shutil, datetime
subprocess.run(['git','add','OUT/FINAL'], check=True)
subprocess.run(['git','commit','-m',f'EKMA+RIR 11.csv ({datetime.date.today()})'], check=True)
subprocess.run(['git','push','origin','master'], check=True)
print('✅ 推送完成')
