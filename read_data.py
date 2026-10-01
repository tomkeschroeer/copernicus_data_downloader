from src.tools import ConfigLoader

from netCDF4 import Dataset

import os
from glob import glob
import zipfile
import argparse

import pandas as pd
import numpy as np

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
    unzipped_folder_path = f"{config.output_path}"
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        os.makedirs(unzipped_folder_path, exist_ok=True)
        zip_ref.extractall(unzipped_folder_path)
        for file in glob(f"{unzipped_folder_path}/*nc"):
            # This extraction expects that the file is saved as cams.eaq.ira.EMPa.var.laltitude.year-month.area-subset.area.nc"
            file_info = file.split("/")[-1].split("cams.eaq.ira.EMPa.")[1].split(".")
            varname = file_info[0]

            data = Dataset(file)
            hours = data.variables["time"][:].data % 24

            # Calculate the number of days in the month
            num_days = len(hours) // 24 
            days = np.repeat(np.arange(1, num_days + 1), 24)
            lat = data.variables["lat"][:]
            lon = data.variables["lon"][:]
            var = data.variables[varname][:]
            file_df = file.replace(".nc",".h5")

            # Expected structure of the data: (time, lat, lon)
            lon = np.tile(np.array(lon), len(data.variables["lat"])*len(data.variables["time"]))
            lat = np.tile(np.repeat(lat, len(data.variables["lon"])), len(data.variables["time"]))
            hours = np.repeat(hours, len(data.variables["lat"])*len(data.variables["lon"]))
            days = np.repeat(days, len(data.variables["lat"])*len(data.variables["lon"]))

            data_dict = {
                "day": days,
                "hour": hours,
                "lat": lat, 
                "lon": lon,
                varname: var.flatten()
                }

            df = pd.DataFrame.from_dict(data_dict)
            df.to_hdf(file_df, key="d")
            data.close()