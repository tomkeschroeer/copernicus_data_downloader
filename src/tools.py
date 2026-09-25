import os
import yaml
import pandas as pd
import numpy as np

class ConfigLoader: 
    """
    A class to load and validate configuration files in YAML format.
    """
    def __init__(
        self, 
        config_path: str = None
    ):
        """
        initialise the config and define the required and optional parameters

        Parameters:
        -----------
        config_path : Optional[str] = None
            path to config file
        """
        # check if file is passed and exists. Raise error otherwise
        if config_path is None:
            raise TypeError(f"No config file passed")
        elif not os.path.exists(config_path):
            raise ValueError(f"config file {config_path} does not exist")

        with open(config_path, 'r') as file:
            try:
                self.config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise ValueError(f"Error parsing YAML file: {exc}")

        # Define which values are expected to be in the config file and which are optional
        self.required_values = [
            "Datasets",
            "output_path"
        ]

        self.required_values_ds = {
            "dataset_name": 'reanalysis-era5-pressure-levels',
            "request": {},
            "target": "download.grib",
        }


    def load_config(self):
        """
        load values defined in config file as attributes
        """
        for val in self.required_values:
            if val not in self.config: raise ValueError(f"value {val} not found but manatory.")
            setattr(self, val, self.config.get(val))

        for ds, value in self.Datasets.items():
            for key, val in self.required_values_ds.items():
                # if key not in self.Datasets[ds]:
                if key not in value.keys():
                    print(f"WARNING: Setting value for \"{key}\" of dataset \"{ds}\" to default value \"{val}\"")
                    self.Datasets[ds][key] = val

