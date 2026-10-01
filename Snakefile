configfile: "snakemake_config.yaml"

rule all:
    input:
        expand("/home/tomke/BNF_GESICA/copernicus_data_downloader/outputs_{var}/{var}_{y}_{m}", var=config["variables"].keys(), y=config["years"], m=config["months"]),
        [
            f"/home/tomke/BNF_GESICA/copernicus_data_downloader/outputs_{var}/"
            f"cams.eaq.ira.EMPa.{var_s}.l50.{y}-{m}.area-subset.46.35.6.35.46.05.5.95.h5"
            for var, var_s in config["variables"].items()
            for y in config["years"]
            for m in config["months"]
        ]

rule all_configs:
    input: 
        expand("/home/tomke/BNF_GESICA/copernicus_data_downloader/configs/config_{var}_{y}.yaml",var=config["variables"].keys(), y=config["years"])

rule write_configs:
    params:
        conf="/home/tomke/BNF_GESICA/copernicus_data_downloader/configs/config",
        out_dir="/home/tomke/BNF_GESICA/copernicus_data_downloader/outputs"
    output:
        expand("/home/tomke/BNF_GESICA/copernicus_data_downloader/configs/config_{var}_{y}.yaml",var=config["variables"].keys(), y=config["years"])
    shell:
        "python write_configs.py -cp {params.conf} -o {params.out_dir} -c snakemake_config.yaml"

rule download:
    input: 
        "/home/tomke/BNF_GESICA/copernicus_data_downloader/configs/config_{var}_{y}.yaml"
    output:
        expand("/home/tomke/BNF_GESICA/copernicus_data_downloader/outputs_{{var}}/{{var}}_{{y}}_{m}", m=config["months"])
    shell:
        "python download_data.py -c {input}"

rule read_data:
    input:
        "/home/tomke/BNF_GESICA/copernicus_data_downloader/configs/config_{var}_{y}.yaml",
        "/home/tomke/BNF_GESICA/copernicus_data_downloader/outputs_{var}/{var}_{y}_{m}"
    output:
        "/home/tomke/BNF_GESICA/copernicus_data_downloader/outputs_{var}/cams.eaq.ira.EMPa.{var_s}.l50.{y}-{m}.area-subset.46.35.6.35.46.05.5.95.h5"
    shell:
        "python read_data.py -c {input[0]} -d ds_{wildcards.m}"
