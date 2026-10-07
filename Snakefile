configfile: "snakemake_config.yaml"
postfix = config.get("postfix", "")
postfix = f"_{postfix}" if postfix else ""

rule all:
    input:
        expand("{base_dir}/outputs_{var}{p}/{var}_{y}_{m}", base_dir=config["base_dir"], p=[postfix], var=config["variables"], y=config["years"], m=config["months"]),
        [
            f"{config['base_dir']}/outputs_{var}{p}/"
            f"cams.eaq.{t}.{mo}.{var_s}.l{l}.{y}-{m}.area-subset.46.35.6.35.46.05.5.95.h5"
            for var, var_s in [(v, config["variables_dict"][v]) for v in config["variables"]]
            for p in [postfix]
            for t in [config["type_dict"][ty] for ty in config.get("type", ["validated_reanalysis"])]
            for mo in [config["model_dict"][mod] for mod in config.get("model", ["validated_reanalysis"])]
            for l in config.get("level", ["50"])
            for y in config["years"]
            for m in config["months"]
        ],
        expand("{base_dir}/outputs_{var}{p}/{var}{p}_merged_files.h5", base_dir=config['base_dir'], p=[postfix], var=config["variables"]),

rule write_configs:
    params:
        conf=f"{config['base_dir']}/configs/",
        out_dir=f"{config['base_dir']}/outputs",
    output:
        expand("{base_dir}/configs/config_{var}_{y}{p}.yaml",base_dir=config['base_dir'], p=[postfix], var=config["variables"], y=config["years"]),
    shell:
        "python write_configs.py -cp {params.conf} -o {params.out_dir} -c snakemake_config.yaml"

rule download:
    input: 
        f"{config['base_dir']}/configs/config_{{var}}_{{y}}{postfix}.yaml"
    output:
        expand("{base_dir}/outputs_{{var}}{p}/{{var}}_{{y}}_{m}", base_dir=config["base_dir"], p=[postfix], m=config["months"])
    shell:
        "python download_data.py -c {input}"

rule read_data:
    input:
        f"{config['base_dir']}/configs/config_{{var}}_{{y}}{postfix}.yaml",
        f"{config['base_dir']}/outputs_{{var}}{postfix}/{{var}}_{{y}}_{{m}}"
    output:
        f"{config['base_dir']}/outputs_{{var}}{postfix}/cams.eaq.{{t}}.{{mo}}.{{var_s}}.l{{l}}.{{y}}-{{m}}.area-subset.46.35.6.35.46.05.5.95.h5",
    shell:
        "python read_data.py -c {input[0]} -d ds_{wildcards.m}"

rule merge:
    input:
        [
            f"{config['base_dir']}/outputs_{var}{p}/"
            f"cams.eaq.{t}.{mo}.{var_s}.l{l}.{y}-{m}.area-subset.46.35.6.35.46.05.5.95.h5"
            for var, var_s in [(v, config["variables_dict"][v]) for v in config["variables"]]
            for p in [postfix]
            for t in [config["type_dict"][ty] for ty in config.get("type", ["validated_reanalysis"])]
            for mo in [config["model_dict"][mod] for mod in config.get("model", ["validated_reanalysis"])]
            for l in config.get("level", ["50"])
            for y in config["years"]
            for m in config["months"]
        ],
    params:
        inp=f"{config['base_dir']}/outputs_{{var}}{postfix}/"
    output:
        f"{config['base_dir']}/outputs_{{var}}{postfix}/{{var}}{postfix}_merged_files.h5"
    shell:
        "python merge_files.py -d {params.inp}"