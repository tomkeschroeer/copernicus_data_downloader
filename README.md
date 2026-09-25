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

<!-- In order to get the area of Geneva, use
```
area: [46.35, 5.95, 46.05, 6.35]
``` -->
Once your download is defined in the config, run:
```
python download_data.py -c path/to/your/config
```