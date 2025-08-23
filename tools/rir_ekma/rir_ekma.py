#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import subprocess
import sys
import argparse
import re  # 添加re模块用于正则表达式

def rir(species, delta):
    # 读取初始配置
    try:
        df_init = pd.read_csv('model/configuration/speciesConstrained.config', 
                             sep=r'\s+', header=None, names=['species', 'concentration'])
        base_row = df_init[df_init['species'] == species]
        if base_row.empty:
            print(f"错误: 物种 {species} 未在约束配置中找到")
            return
        base = float(base_row['concentration'].iloc[0])
    except Exception as e:
        print(f"读取约束配置时出错: {e}")
        return
    
    # 创建输出目录
    os.makedirs('OUT_BATCH', exist_ok=True)
    
    # 运行不同扰动强度的模拟
    for factor in [1-delta, 1+delta]:
        # 修改浓度
        df_mod = df_init.copy()
        df_mod.loc[df_mod['species'] == species, 'concentration'] = base * factor
        
        # 保存修改后的配置
        df_mod.to_csv('model/configuration/speciesConstrained.config', 
                     sep=' ', header=False, index=False)
        
        # 运行模拟
        try:
            result = subprocess.run(['./atchem2'], check=True, capture_output=True, text=True, timeout=300)
            print(f"模拟输出: {result.stdout}")
            if result.stderr:
                print(f"模拟错误: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"运行atchem2时出错: {e}")
            print(f"错误输出: {e.stderr}")
            continue
        except subprocess.TimeoutExpired:
            print("模拟超时")
            continue
        
        # 保存结果
        if os.path.exists('output/output.concentrations.csv'):
            os.rename('output/output.concentrations.csv', f'OUT_BATCH/output_{factor}.csv')
            print(f"完成因子 {factor} 的模拟")
        else:
            print(f"警告: 输出文件不存在 for factor {factor}")
            print("检查output目录内容:")
            if os.path.exists('output'):
                print(os.listdir('output'))

def ekma(nox_seq):
    # 读取初始配置
    try:
        df_init = pd.read_csv('model/configuration/speciesConstrained.config', 
                             sep=r'\s+', header=None, names=['species', 'concentration'])
        
        # 检查NO和NO2是否存在
        no_row = df_init[df_init['species'] == 'NO']
        no2_row = df_init[df_init['species'] == 'NO2']
        
        if no_row.empty or no2_row.empty:
            print("错误: NO 或 NO2 未在约束配置中找到")
            return
            
        base_no = float(no_row['concentration'].iloc[0])
        base_no2 = float(no2_row['concentration'].iloc[0])
    except Exception as e:
        print(f"读取约束配置时出错: {e}")
        return
    
    # 创建输出目录
    os.makedirs('OUT_BATCH', exist_ok=True)
    
    # 运行不同NOx水平的模拟
    for i, f in enumerate(nox_seq):
        df_mod = df_init.copy()
        df_mod.loc[df_mod['species'] == 'NO', 'concentration'] = base_no * f
        df_mod.loc[df_mod['species'] == 'NO2', 'concentration'] = base_no2 * f
        
        # 保存修改后的配置
        df_mod.to_csv('model/configuration/speciesConstrained.config', 
                     sep=' ', header=False, index=False)
        
        # 运行模拟
        try:
            result = subprocess.run(['./atchem2'], check=True, capture_output=True, text=True, timeout=300)
            print(f"模拟输出: {result.stdout}")
            if result.stderr:
                print(f"模拟错误: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"运行atchem2时出错: {e}")
            print(f"错误输出: {e.stderr}")
            continue
        except subprocess.TimeoutExpired:
            print("模拟超时")
            continue
        
        # 保存结果
        if os.path.exists('output/output.concentrations.csv'):
            os.rename('output/output.concentrations.csv', f'OUT_BATCH/output_nox_{i}.csv')
            print(f"完成NOx因子 {f} 的模拟")
        else:
            print(f"警告: 输出文件不存在 for NOx factor {f}")
            print("检查output目录内容:")
            if os.path.exists('output'):
                print(os.listdir('output'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run RIR or EKMA analysis')
    parser.add_argument('--mode', choices=['rir', 'ekma'], required=True)
    parser.add_argument('--species', help='Species for RIR analysis')
    parser.add_argument('--delta', type=float, help='Perturbation delta for RIR')
    parser.add_argument('--nox_seq', nargs='+', type=float, help='NOx scaling factors for EKMA')
    
    args = parser.parse_args()
    
    if args.mode == 'rir':
        if not args.species or not args.delta:
            print("错误: RIR模式需要--species和--delta参数")
            sys.exit(1)
        rir(args.species, args.delta)
    elif args.mode == 'ekma':
        if not args.nox_seq:
            print("错误: EKMA模式需要--nox_seq参数")
            sys.exit(1)
        ekma(args.nox_seq)
