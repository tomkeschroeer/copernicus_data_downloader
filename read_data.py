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
    unzipped_folder_path = f"{path_to_zip_file}_unzipped"
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        os.makedirs(unzipped_folder_path, exist_ok=True)
        zip_ref.extractall(unzipped_folder_path)
        for file in glob(f"{unzipped_folder_path}/*nc"):
            # This extraction expects that the file is saved as cams.eaq.ira.EMPa.var.laltitude.year-month.area-subset.area.nc"
            file_info = file.split("/")[-1].split("cams.eaq.ira.EMPa.")[1].split(".")
            varname = file_info[0]
            year = file_info[2].split("-")[0]
            month = file_info[2].split("-")[1]
            data = Dataset(file)
            hours = data.variables["time"][:].data % 24
            # Calculate the number of days in the month
            num_days = len(hours) // 24 
            days = np.repeat(np.arange(1, num_days + 1), 24)
            lat = data.variables["lat"][:]
            lon = data.variables["lon"][:]
            var = data.variables[varname][:]
            file_df = file.replace(".nc", ".h5")
            panddat = pd.read_hdf(file_df)
            breakpoint()
            for i, dim in enumerate(data.dimensions.keys()):
                if dim == "time":
                    lon = np.repeat(lon, len(data.variables[dim][:]))
                    lat = np.repeat(lat, len(data.variables[dim][:]))
                elif dim == "lat":
                    days = np.repeat(days, len(data.variables[dim][:]))
                    hours = np.repeat(hours, len(data.variables[dim][:]))
                    lon = np.repeat(lon, len(data.variables[dim][:]))
                elif dim == "lon":
                    days = np.repeat(days, len(data.variables[dim][:]))
                    hours = np.repeat(hours, len(data.variables[dim][:]))
                    lat = np.repeat(lat, len(data.variables[dim][:]))
            data_dict = {
                "day": days,
                "hour": hours,
                "lat": lat, 
                "lon": lon,
                varname: var.flatten()
                }
            df = pd.DataFrame.from_dict(data_dict)
            
            df.to_hdf(file_df, key="d")
            # data.variables["co"]
            data.close()




    # nc_data = Dataset("./cams.eaq.ira.EMPa.co.l50.2024-02.area-subset.46.35.6.35.46.05.5.95.nc", mode='r')

    # # Print the file's metadata
    # print(nc_data)

    # # Access variables or dimensions
    # print(nc_data.variables.keys())  # List all variables
    # print(nc_data.dimensions.keys())  # List all dimensions
    # breakpoint()
    # # Close the file when done
    # nc_data.close()
    # # print(ds.latitude)
