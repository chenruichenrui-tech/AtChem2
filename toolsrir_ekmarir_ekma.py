#!/usr/bin/env python3
"""
rir_ekma.py  ——  为 AtChem2 批量生成 RIR/EKMA 曲线
依赖：pandas, numpy, matplotlib, seaborn
用法：
    python tools/rir_ekma/rir_ekma.py --mode rir   --species CH4 --delta 0.2
    python tools/rir_ekma/rir_ekma.py --mode ekma  --nox_seq 0.1 0.2 0.5 1 2 5 10
"""
import pandas as pd, numpy as np, os, argparse, shutil, subprocess, matplotlib.pyplot as plt, seaborn as sns

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.join(BASE_DIR, '..', '..')
MODEL_EXE  = os.path.join(ROOT_DIR, 'atchem2')
CFG_DIR    = os.path.join(ROOT_DIR, 'model', 'configuration')

def read_conc():
    df = pd.read_csv(os.path.join(ROOT_DIR, 'OUT', 'speciesConcentrations.output'),
                     delim_whitespace=True, comment='#')
    return df['O3'].max()

def run_once(tag):
    subprocess.run(MODEL_EXE, cwd=ROOT_DIR, check=True)
    o3 = read_conc()
    os.makedirs(os.path.join(ROOT_DIR, 'OUT_BATCH'), exist_ok=True)
    shutil.copytree(os.path.join(ROOT_DIR, 'OUT'),
                    os.path.join(ROOT_DIR, 'OUT_BATCH', tag))
    return o3

def rir(species, delta):
    df_init = pd.read_csv(os.path.join(CFG_DIR, 'speciesConstrained.config'), delim_whitespace=True, header=None)
    base = float(df_init[df_init[0]==species][1])
    # baseline
    o3_base = run_once('base')
    # perturbed
    df_init.loc[df_init[0]==species, 1] = base*(1+delta)
    df_init.to_csv(os.path.join(CFG_DIR, 'speciesConstrained.config'), sep=' ', index=False, header=False)
    o3_new = run_once(f'{species}+{delta}')
    rir_val = (o3_new - o3_base) / (delta * base) * base
    print(f'RIR({species}) = {rir_val:.3f}')
    return rir_val

def ekma(nox_seq):
    res = []
    for f in nox_seq:
        df = pd.read_csv(os.path.join(CFG_DIR, 'speciesConstrained.config'), delim_whitespace=True, header=None)
        df.loc[df[0]=='NO', 1] = float(df[df[0]=='NO'][1]) * f
        df.loc[df[0]=='NO2', 1] = float(df[df[0]=='NO2'][1]) * f
        df.to_csv(os.path.join(CFG_DIR, 'speciesConstrained.config'), sep=' ', index=False, header=False)
        o3 = run_once(f'NOx{x}')
        res.append((f, o3))
    df = pd.DataFrame(res, columns=['NOx_factor','O3'])
    sns.lineplot(data=df, x='NOx_factor', y='O3')
    plt.xscale('log')
    plt.title('EKMA curve')
    plt.savefig(os.path.join(ROOT_DIR, 'OUT_BATCH', 'ekma.png'))
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['rir','ekma'], required=True)
    parser.add_argument('--species')
    parser.add_argument('--delta', type=float, default=0.2)
    parser.add_argument('--nox_seq', nargs='+', type=float, default=[0.1,0.3,1,3,10])
    args = parser.parse_args()
    if args.mode == 'rir':
        rir(args.species, args.delta)
    else:
        ekma(args.nox_seq)