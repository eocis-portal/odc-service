# odc-service - Installation Recipe

## As the `root` user

### Create a service account `dev`

```bash
useradd dev -m -s /bin/bash
usermod -aG sudo dev
```

### rsync in some data

```bash
mkdir -p /data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1
cd /data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1
rsync -av niallmcc@xfer1.jasmin.ac.uk:/gws/nopw/j04/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1/2021 .
chmod -R a+rwx /data/esacci_sst
```

## As the `dev` user

### install miniconda

```bash
wget --no-proxy https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod u+x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

### create conda environment `odc_env`

```bash
sudo apt-get install libgdal-dev libhdf5-serial-dev libnetcdf-dev
conda config --append channels conda-forge
conda create --name odc_env python=3.9 datacube
conda activate odc_env
conda install -c anaconda postgresql
conda install jupyter matplotlib scipy
```

### clone repo

```bash
git clone https://github.com/eocis-portal/odc-service.git
```

### create database, start database service

```bash
conda activate odc_env
cd github/odc-service/scripts/db
./create.sh
./start.sh
./status.sh
```

### Initialise datacube

```bash
conda activate odc_env
cp github/odc-service/config/datacube.conf ~/.datacube.conf
cd ~
datacube -C ~/.datacube.conf system init
```

### install custom drivers

```bash
cd ~/github/odc-service
pip install .
```

### load SST product 

```bash
cd github/odc-service/product_definitions/sst
datacube -C ~/.datacube.conf product add sst.yaml
```

### Generate SST dataset definitions for each netcdf

```bash
python sst_importer.py --input-folder /data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1 --start-date 1980-01-01 --end-date 2021-12-31
# to add a single year
./add.sh 2021
rm -rf 2021

# to add multiple years in the background
rm nohup.out # if it exists
nohup ./add_multi.sh 1980 2020 &
```

### Patch datacube to assign EPSG:4326 to imported netcdf4 files by default

```bash
vi ~/miniconda3/envs/odc_env/lib/python3.9/site-packages/datacube/storage/_rio.py
```

Edit the function `_rasterio_crs`:

```python
def _rasterio_crs(src):
    if src.crs is None:
        return rasterio.CRS.from_epsg(4326)
        # raise ValueError('no CRS')

    return geometry.CRS(src.crs)
```

### Install OWS

```bash
conda install pre_commit
conda install postgis
pip install datacube-ows[all]
```

### Setup POSTGIS extension

```
psql -d odc
create extension postgis;
\q
```

### Setup OWS

```bash
cd github/odc-service/ows
. ./ows_env.sh
datacube-ows-update --schema --role dev
datacube-ows-update --view
datacube-ows-update sst
```

### Start OWS flask service

```bash
cd ~/github/odc-service/ows/
. ./ows_env.sh
flask run -h 0.0.0.0
```

