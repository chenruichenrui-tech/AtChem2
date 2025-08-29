import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
from scipy.interpolate import griddata
plt.rcParams['font.family']='DejaVu Sans'
df=pd.read_csv('OUT/11_processed.csv')
voc=df['total_VOC_ppb']; nox=df['total_NOx_ppb']; o3=df['O3_ppb']
v=np.linspace(voc.min(),voc.max(),100); n=np.linspace(nox.min(),nox.max(),100)
V,N=np.meshgrid(v,n); Z=griddata((voc,nox),o3,(V,N),method='cubic')

# 跳过 NaN 列
ridge=[]
for i,vv in enumerate(v):
    col=Z[:,i]
    if np.all(np.isnan(col)): continue
    j=np.nanargmax(col)
    ridge.append([vv,n[j]])
ridge=np.array(ridge)

slopes=np.diff(ridge[:,1])/np.diff(ridge[:,0])
regime='VOC-Limited' if np.nanmean(np.abs(slopes))>3 else \
       'NOx-Limited' if np.nanmean(np.abs(slopes))<0.8 else 'Transition'

fig,ax=plt.subplots(figsize=(12,9))
cs=ax.contourf(V,N,Z,cmap='viridis'); plt.colorbar(cs,label='O3 (ppb)')
ax.plot(ridge[:,0],ridge[:,1],'r-',label='Ridge')
ax.scatter(ridge[::5,0],ridge[::5,1],marker='^',s=120,color='yellow',edgecolors='k')
ax.text(0.75,0.15,regime,transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.5",facecolor='red' if 'VOC' in regime else 'blue',alpha=0.7))
ax.set_xlabel('VOC (ppb)'); ax.set_ylabel('NOx (ppb)')
ax.set_title('EKMA Curve & Control Regime'); ax.grid(False); ax.legend()
plt.tight_layout(); plt.savefig('OUT/FINAL/final_ekma_curve.png')
print('✅ 03 EKMA完成')
