import cdsapi
import argparse
import os

from src.tools import ConfigLoader

client = cdsapi.Client()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, help="path to config file", required=True)
args = parser.parse_args()
config_path = args.config

config = ConfigLoader(config_path)
config.load_config()

# check if output directory exists and create it if not
os.makedirs(config.output_path, exist_ok = True)

# loop through datasets and download them
for dataset in config.Datasets.values():
  target = (f"{config.output_path}/" + dataset["target"]).replace("//","/")
  client.retrieve(dataset["dataset_name"], dataset["request"], target)