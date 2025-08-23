import pandas as pd, matplotlib.pyplot as plt, numpy as np
plt.rcParams['font.family']='DejaVu Sans'
df=pd.read_csv('OUT/11_processed.csv'); df['time']=pd.to_datetime(df['time'])
fig,axes=plt.subplots(4,1,figsize=(15,10),sharex=True)
for ax,col,lab in zip(axes,['O3_ppb','total_NOx_ppb','total_VOC_ppb','temperature_C'],['O3','NOx','VOC','Temp']):
    ax.plot(df['time'],df[col]); ax.set_ylabel(lab); ax.grid(False)
plt.xticks(rotation=45); plt.tight_layout(); plt.savefig('OUT/FINAL/final_time_series.png')

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(14,5))
ax1.scatter(df['total_VOC_ppb'],df['total_NOx_ppb'],c=df['O3_ppb'],cmap='plasma',s=30); ax1.set_xlabel('VOC'); ax1.set_ylabel('NOx'); ax1.set_title('VOC vs NOx'); ax1.grid(False)
ax2.scatter(df['total_VOC_ppb']/df['total_NOx_ppb'],df['O3_ppb'],s=30); ax2.set_xlabel('VOC/NOx'); ax2.set_ylabel('O3'); ax2.set_title('O3 vs Ratio'); ax2.grid(False)
plt.tight_layout(); plt.savefig('OUT/FINAL/final_relationships.png')
print('✅ 04 时间/关系图完成')
