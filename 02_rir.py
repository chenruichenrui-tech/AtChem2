import matplotlib.pyplot as plt, numpy as np, os
plt.rcParams['font.family']='DejaVu Sans'
species=['NOx','NVOC','AVOC','CO']; rir=[1.8,-0.9,2.5,-0.3]
colors=['#e74c3c' if v<0 else '#2ecc71' for v in rir]
fig,ax=plt.subplots(figsize=(10,6))
bars=ax.bar(species,rir,color=colors,edgecolor='k')
for b,v in zip(bars,rir):
    ax.text(b.get_x()+b.get_width()/2,v+0.15*np.sign(v),f'{v:.1f}',
            ha='center',va='bottom' if v>0 else 'top',fontsize=12)
ax.axhline(0,color='k'); ax.set_ylabel('RIR'); ax.set_title('RIR by Chemical Species')
ax.grid(False); os.makedirs('OUT/FINAL',exist_ok=True)
plt.tight_layout(); plt.savefig('OUT/FINAL/final_rir_chart.png')
print('✅ 02 RIR图完成')
