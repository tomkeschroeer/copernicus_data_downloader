configfile: "snakemake_config.yaml"
base_dir = config["base_dir"]

rule all:
    params:
        base_dir = config["base_dir"]
    input:
        expand("{base_dir}/outputs_{var}/{var}_{y}_{m}", base_dir=config["base_dir"], var=config["variables"].keys(), y=config["years"], m=config["months"]),
        [
            f"{config['base_dir']}/outputs_{var}/"
            f"cams.eaq.ira.EMPa.{var_s}.l50.{y}-{m}.area-subset.46.35.6.35.46.05.5.95.h5"
            for var, var_s in config["variables"].items()
            for y in config["years"]
            for m in config["months"]
        ],
        expand("{base_dir}/outputs_{var}/{var}_merged_files.h5", base_dir=config['base_dir'], var=config["variables"].keys()),

rule write_configs:
    params:
        conf=f"{config['base_dir']}/configs/config",
        out_dir=f"{config['base_dir']}/outputs",
    output:
        expand("{base_dir}/configs/config_{var}_{y}.yaml",base_dir=config['base_dir'], var=config["variables"].keys(), y=config["years"]),
    shell:
        "python write_configs.py -cp {params.conf} -o {params.out_dir} -c snakemake_config.yaml"

rule download:
    params:
        base_dir = config["base_dir"]
    input: 
        f"{config['base_dir']}/configs/config_{{var}}_{{y}}.yaml"
    output:
        expand("{base_dir}/outputs_{{var}}/{{var}}_{{y}}_{m}", base_dir=config["base_dir"], m=config["months"])
    shell:
        "python download_data.py -c {input}"

rule read_data:
    input:
        f"{config['base_dir']}/configs/config_{{var}}_{{y}}.yaml",
        f"{config['base_dir']}/outputs_{{var}}/{{var}}_{{y}}_{{m}}"
    output:
        f"{config['base_dir']}/outputs_{{var}}/cams.eaq.ira.EMPa.{{var_s}}.l50.{{y}}-{{m}}.area-subset.46.35.6.35.46.05.5.95.h5"
    shell:
        "python read_data.py -c {input[0]} -d ds_{wildcards.m}"

rule merge:
    input:
        f"{config['base_dir']}/outputs_{{var}}"
    output:
        f"{config['base_dir']}/outputs_{{var}}/{{var}}_merged_files.h5"
    shell:
        "python merge_files.py -d {input}"