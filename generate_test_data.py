import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 创建时间序列（5天，逐小时）
start_date = datetime(2023, 6, 1, 0, 0, 0)
end_date = start_date + timedelta(days=5)
time_series = pd.date_range(start=start_date, end=end_date, freq='H')[:-1]  # 排除最后一个时间点

# 创建基本数据结构
data = {
    '时间': time_series,
    '温度_℃': np.random.normal(25, 5, len(time_series)),
    '相对湿度_%': np.random.uniform(40, 90, len(time_series)),
    '风速_m/s': np.random.uniform(0.5, 5.0, len(time_series)),
    '气压_hPa': np.random.normal(1013, 10, len(time_series)),
    '太阳辐射_W/m2': np.zeros(len(time_series)),
    'O3_ppb': np.zeros(len(time_series)),
    'NOx_ppb': np.zeros(len(time_series)),
    'VOC_ppb': np.zeros(len(time_series)),
    'CO_ppb': np.zeros(len(time_series)),
    'PM2.5_μg/m3': np.zeros(len(time_series))
}

# 创建DataFrame
df = pd.DataFrame(data)

# 添加日变化模式
for i, time in enumerate(time_series):
    hour = time.hour
    
    # 太阳辐射（白天高，夜晚低）
    if 6 <= hour <= 18:
        df.loc[i, '太阳辐射_W/m2'] = np.random.uniform(200, 800)
    
    # O3浓度（白天光化学反应生成）
    if 10 <= hour <= 16:
        df.loc[i, 'O3_ppb'] = np.random.uniform(30, 80)
    else:
        df.loc[i, 'O3_ppb'] = np.random.uniform(10, 40)
    
    # NOx浓度（早晚高峰）
    if (7 <= hour <= 9) or (17 <= hour <= 19):
        df.loc[i, 'NOx_ppb'] = np.random.uniform(20, 50)
    else:
        df.loc[i, 'NOx_ppb'] = np.random.uniform(5, 20)
    
    # VOC浓度（与人类活动相关）
    if 8 <= hour <= 20:
        df.loc[i, 'VOC_ppb'] = np.random.uniform(10, 30)
    else:
        df.loc[i, 'VOC_ppb'] = np.random.uniform(5, 15)
    
    # CO浓度
    df.loc[i, 'CO_ppb'] = np.random.uniform(0.1, 2.0)
    
    # PM2.5浓度
    df.loc[i, 'PM2.5_μg/m3'] = np.random.uniform(10, 60)

# 添加一些趋势和异常值
df.loc[20:30, 'O3_ppb'] *= 1.5  # 增加一段时间的O3浓度
df.loc[40:45, 'PM2.5_μg/m3'] *= 2.0  # 增加一段时间的PM2.5浓度
df.loc[70:75, 'NOx_ppb'] *= 0.5  # 减少一段时间的NOx浓度

# 保存为CSV文件
df.to_csv('12.csv', index=False, encoding='utf-8-sig')

print(f"已生成测试数据文件 12.csv，包含 {len(df)} 行数据")
print("列名:", df.columns.tolist())
print("时间范围:", df['时间'].min(), "至", df['时间'].max())
