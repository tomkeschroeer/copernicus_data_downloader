import yaml
import argparse
from copy import deepcopy
import os

parser = argparse.ArgumentParser()

parser.add_argument("-cp", "--config_path", type=str, help="path where to save config file", required=True)
parser.add_argument("-o", "--outputdir", type=str, help="name of directory to save files", required=True)
parser.add_argument("-c", "--config_file", type=str, help="config file that defines which months to consider, the years and the variables.", required=True)

args = parser.parse_args()
config_path = args.config_path
output_dir = args.outputdir
config_file = args.config_file

config_path = (config_path.replace(".yaml","") + "/config").replace("//","/")

if config_file is None:
    raise TypeError(f"No config_file file passed")
elif not os.path.exists(config_file):
    raise ValueError(f"config file {config_file} does not exist")

with open(config_file, 'r') as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise ValueError(f"Error parsing YAML file: {exc}")

months_to_consider = config["months"]
vars_to_consider = list(config["variables"].keys())
years_to_consider = config["years"]

config_data = {
    "output_path": output_dir,
    "Datasets": {}
    }

def_dataset =  {
            "dataset_name": "cams-europe-air-quality-reanalyses",
            "request": {
                "variable": [],
                "model": config.get("model","emep"),
                "level": config.get("level","50"),
                "type": config.get("type","interim_reanalysis"),
                "year": [],
                "month": [],
                "area": config.get("area",[46.35, 5.95, 46.05, 6.35])
            },
            "target": None
        }

for y in years_to_consider:
    def_dataset["request"]["year"] = [y]
    for v in vars_to_consider:
        def_dataset["request"]["variable"] = [v]
        for m in months_to_consider:
            mod_dataset = deepcopy(def_dataset)
            mod_dataset["request"]["month"] = [m]
            mod_dataset["target"] = f"{v}_{y}_{m}"
            config_data["Datasets"][f"ds_{m}"] = mod_dataset
        config_data["output_path"] = f"{output_dir}_{v}" if config.get("postfix", None) is None else f"{output_dir}_{v}_{config['postfix']}"
            # breakpoint()
        
        conf_path = f'{config_path}_{v}_{y}.yaml' if config.get("postfix", None) is None else f"{config_path}_{v}_{y}_{config['postfix']}.yaml"
        with open(conf_path, 'w') as outfile:
            yaml.dump(config_data, outfile, default_flow_style=None)

