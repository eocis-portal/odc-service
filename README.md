# odc-service

```bash
sudo apt-get install libgdal-dev libhdf5-serial-dev libnetcdf-dev
conda config --append channels conda-forge
conda create --name odc_env python=3.7 datacube
conda activate odc_env
conda install -c anaconda postgresql
conda install jupyter matplotlib scipy
```

```bash
git clone https://github.com/opendatacube/datacube-core
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

# Initialise datacube

```bash
conda activate odc_env
cp github/odc-service/config/datacube.conf ~/.datacube.conf
cd ~
datacube -C ~/.datacube.conf system init
```

# load SST product and dataset(s)

```bash
cd github/odc-service/product_definitions/sst
datacube -C ~/.datacube.conf product add sst.yaml

python sst_importer.py --input-folder /data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1 --start-date 2021-01-01 --end-date 2021-12-31
./add.sh 2021
rm -rf 2021
```

```bash
vi ~/miniconda3/envs/odc_env/lib/python3.7/site-packages/datacube/storage/_rio.py
```

Edit the function `_rasterio_crs`:

```python
def _rasterio_crs(src):
    if src.crs is None:
        return rasterio.CRS.from_epsg(4326)
        # raise ValueError('no CRS')

    return geometry.CRS(src.crs)
```

