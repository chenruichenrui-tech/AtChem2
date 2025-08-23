import pandas as pd
import os
df = pd.read_csv('11.csv')
mapping = {'时间':'time','茅山头O3':'O3_ppb','茅山头CO':'CO_ppb',
           '茅山头NO2':'NO2_ppb','NO':'NO_ppb','2m温度℃':'temperature_C',
           '异戊二烯':'isoprene_ppb','乙烷':'ethane_ppb','丙烷':'propane_ppb',
           '正丁烷':'n_butane_ppb','异丁烷':'i_butane_ppb','乙烯':'ethylene_ppb',
           '丙醛':'propanal_ppb','丙烯':'propylene_ppb','甲苯':'toluene_ppb',
           '间、对-二甲苯':'xylene_ppb','丙酮':'acetone_ppb'}
df = df.rename(columns=mapping)
voc_cols = [c for c in df.columns if '_ppb' in c and c not in ['O3_ppb','NO2_ppb','NO_ppb']]
df['total_VOC_ppb'] = df[voc_cols].sum(axis=1)
df['total_NOx_ppb'] = df['NO_ppb'] + df['NO2_ppb']
os.makedirs('OUT', exist_ok=True)
df.to_csv('OUT/11_processed.csv', index=False)
print('✅ 01 预处理完成')
