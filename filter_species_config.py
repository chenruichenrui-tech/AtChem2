import pathlib

print("过滤配置文件中的物种...")

# 读取化学机制中的物种
species_in_mechanism = set()
mechanism_species_file = "mechanism/mechanism.species"
if pathlib.Path(mechanism_species_file).exists():
    with open(mechanism_species_file, "r") as f:
        for line in f:
            species = line.strip()
            if species:
                species_in_mechanism.add(species)
    print(f"化学机制中包含 {len(species_in_mechanism)} 个物种")
else:
    print(f"错误: 找不到 {mechanism_species_file} 文件")
    exit(1)

# 过滤 speciesConstant.config
constant_config = "model/configuration/speciesConstant.config"
constant_content = []
constant_removed = []
if pathlib.Path(constant_config).exists():
    with open(constant_config, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                species_name = parts[0]
                if species_name in species_in_mechanism:
                    constant_content.append(line)
                else:
                    constant_removed.append(species_name)
    
    # 写入过滤后的内容
    with open(constant_config, "w") as f:
        f.writelines(constant_content)
    
    print(f"从 speciesConstant.config 中移除了 {len(constant_removed)} 个物种: {', '.join(constant_removed)}")
else:
    print(f"警告: 找不到 {constant_config}")

# 过滤 speciesConstrained.config
constrained_config = "model/configuration/speciesConstrained.config"
constrained_content = []
constrained_removed = []
if pathlib.Path(constrained_config).exists():
    with open(constrained_config, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                species_name = parts[0]
                if species_name in species_in_mechanism:
                    constrained_content.append(line)
                else:
                    constrained_removed.append(species_name)
    
    # 写入过滤后的内容
    with open(constrained_config, "w") as f:
        f.writelines(constrained_content)
    
    print(f"从 speciesConstrained.config 中移除了 {len(constrained_removed)} 个物种: {', '.join(constrained_removed)}")
else:
    print(f"警告: 找不到 {constrained_config}")

print("配置文件过滤完成!")
