
import argparse
from glob import glob
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", type=str, help="directory to merge files", required=True)
args = parser.parse_args()
directory = args.directory

files_to_merge = sorted(glob(f"{directory}/cams*.h5"))

df_complete = None

for file in files_to_merge:
    subcon = file.split("cams")[1].split(".")
    year = subcon[6].split("-")[0]
    month = subcon[6].split("-")[1]
    df = pd.read_hdf(file)
    df["month"] = np.repeat(month, len(df))
    df["year"] = np.repeat(year, len(df))
    if df_complete is None:
        df_complete = df
    else:
        df_complete = pd.concat((df_complete, df))
variable = directory.split("/outputs_")[-1]
df_complete.to_hdf(f"{directory}/{variable}_merged_files.h5", key="d")
