import yaml
import argparse
from copy import deepcopy

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", type=str, help="name of config file", required=True)
parser.add_argument("-o", "--outputdir", type=str, help="name of directory to safe files", required=False)

args = parser.parse_args()
config_name = args.config
output_dir = args.outputdir

config_dictionary = "./configs"

months_to_consider = [
    "01", "02", "03",
    "04", "05", "06",
    "07", "08", "09",
    "10", "11", "12"
]

vars_to_consider = [
    "carbon_monoxide",
    "nitrogen_dioxide"
    # "ozone",
    # "particulate_matter_2.5um",
    # "particulate_matter_10um",
    # "sulphur_dioxide"
]

years_to_consider = [
    "2022", "2023", 
    # "2024", "2025", 
    # "2026"
]

config_data = {
    "output_path": output_dir,
    "Datasets": {}
    }

def_dataset =  {
            "dataset_name": "cams-europe-air-quality-reanalyses",
            "request": {
                "variable": [],
                "model": ["emep"],
                "level": ["50"],
                "type": ["interim_reanalysis"],
                "year": [],
                "month": [],
                "area": [46.35, 5.95, 46.05, 6.35]
            },
            "target": "two_vars"
        }

for y in years_to_consider:
    def_dataset["request"]["year"] = [y]
    for v in vars_to_consider:
        def_dataset["request"]["variable"] = [v]
        def_dataset["output_path"] = f"{output_dir}_{v}_{y}"
        for m in months_to_consider:
            mod_dataset = deepcopy(def_dataset)
            mod_dataset["request"]["month"] = [m]
            mod_dataset["target"] = f"{v}_{y}_{m}"
            config_data["Datasets"][f"ds_{m}"] = mod_dataset
            # breakpoint()
    
    with open(f'{config_dictionary}/{config_name}_{v}_{y}.yaml', 'w') as outfile:
        yaml.dump(config_data, outfile,default_flow_style=None)

