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