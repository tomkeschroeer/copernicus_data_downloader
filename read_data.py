from src.tools import ConfigLoader

from netCDF4 import Dataset
import os
import zipfile
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", type=str, help="path to config file", required=True)
parser.add_argument("-d", "--datasets", type=str, help="name of dataset to unzip", required=False)

args = parser.parse_args()
config_path = args.config
datasets = args.datasets

config = ConfigLoader(config_path)
config.load_config()

if datasets is not None:
    datasets = args.datasets.split(",")
else:
    print(f"WARNING: No dataset given. Unzipping all.")
    datasets = list(config.Datasets.keys())

for ds in datasets:
    if ds not in config.Datasets.keys():
        print(f"WARNING: dataset {ds} is not present in your config file. Skipped.")
        continue
    current_target = config.Datasets[ds]["target"]
    path_to_zip_file = f"{config.output_path}/{current_target}".replace("//","/'")
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        os.makedirs(f"{path_to_zip_file}_unziped", exist_ok=True)
        zip_ref.extractall(f"{path_to_zip_file}_unziped")
