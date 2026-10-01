# Copernicus data downloader
Little repo to download data from the Copernicus datasets using the Climate Data Store API (CDSAPI)
## Prequisite
The code was tested using Python 3.10.18

### Getting the code
Get the code by cloning the repository from github:
```
git clone git@github.com:tomkeschroeer/copernicus_data_downloader.git
```
and enter the folder:
```
cd copernicus_data_downloader
```

### Installing the needed packages
To use the code install the packages defined in `requirements.txt`. In order to use a virtual environment, execute the following commands.
Create the virtual environment:
```
python3 -m venv cop_env
```
This create a folder called `cop_env`. You can also choose to create the virtual environment in a different folder. In that case replace `cop_env` here and in the following by the path to your preferred folder.
Activate the environment:
```
source cop_env/bin/activate
```
Install the requirements:
```bash
python3 -m pip install -r requirements.txt
```
## Getting data
Before getting started with this repository you need some preparation. The CAMS European air quality reanalysis dataset that contains data about the near-surface pollution concentration. To use the API to download data from thos dataset you need to follow the instruction given [here](https://ads.atmosphere.copernicus.eu/how-to-api).

Once this was setup, you can configure the download yourself or use [this website](https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-reanalyses?tab=download) to give you the API command. 

In order to get the area of Geneva, use
```
area: [46.35, 5.95, 46.05, 6.35]
```
Once your download is defined in the config, run:
```
python download_data.py -c path/to/your/config
```
This downloads a zip folder that contains the files in a NetCDF format, sorted by area and month. 

The variables are each stored in a separate file in a 3-dimensional array with the dimensions `(time, longitude, latidute)`. The time is stored as the hour of the month. The data is stored separately per month. The variable `time` has therefore $24\cdot N_{days}$ entries with $N_{days}$ being the number of days in the month considered.

To help writing the config files, the script `write_configs` can be used. For this, a minimal set of parameters need to be passed through a config file. The following arguments have to be defined:

| Variable | Description <div style="width:330px">| Potential Values |
|----------|---------------------|----------|
| variables | dictionary of the names of variables and the short format as variable:short form | \{"ozone": "o3", "nitrogen_dioxide":"no2", "particulate_matter_2.5um": "pm2p5", "particulate_matter_10um": "pm10", "sulphur_dioxide": "so2" \} |
| years | years to download as strings | \["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025" \] |
| months | months to diwnload as strings | \["01","02","03","04","05","06","07',"08","09","10","11","12"\]

In addition the `level`, `type`, `model` can be set, possible values can be found [here](https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-reanalyses?tab=download).

In order to store the data in a zip folder with `nc` file, run 
```
python download_data.py -c path/to/your/config -d names,of,datasets,to,process
```
If all datasets should be transformed into an `h5` file, the `-d` flag can be dropped. Afterwards, the files in one output folder can also be merged into one file by adding the year and month as extra columns. Run:
In order to store the data in an `h5` file, run 
```
python merge_files.py -d path/to/your/directory/with/files/to/merge
```
If all scripts should be performed automatically, you can use snakemake. Define the datasets you would like to download in the `snakemake_config.yaml`. If you use this the first time, run
```
source setup.sh
```
afterwards, run
```
snakemake
```
This writes the configs, downloads all files, transformes them and merges them into one file per variable.