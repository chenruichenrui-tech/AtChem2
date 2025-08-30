import subprocess
import datetime
import os

print("推送结果到GitHub...")

# 添加所有文件
subprocess.run(['git', 'add', '-A'], check=True)

# 提交
commit_message = f"AtChem2分析结果 ({datetime.date.today()})"
subprocess.run(['git', 'commit', '-m', commit_message], check=True)

# 推送
result = subprocess.run(['git', 'push', 'origin', 'master'], capture_output=True, text=True)

if result.returncode == 0:
    print("✅ 推送成功")
else:
    print("❌ 推送失败，尝试强制推送")
    subprocess.run(['git', 'push', 'origin', 'master', '--force'], check=True)
    print("✅ 强制推送成功")
