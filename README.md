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
cd datacube-core/
conda activate odc_env
```