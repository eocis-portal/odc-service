import rasterio

import datetime

def get_date(filename):
    splits = filename.split("/")
    y = splits[-4]
    m = splits[-3]
    d = splits[-2]
    dt = datetime.date(int(y),int(m),int(d))
    doy = dt.timetuple().tm_yday
    if doy == 366:
        doy = 365
    return doy



filename = "NetCDF:/home/dev/data/regrid/sst/2022/01/02/20220101120000-C3S-L4_GHRSST-SSTdepth-OSTIA-GLOB_ICDR3.0-v02.0-fv01.0.nc:analysed_sst"
import sys
print(get_date(filename))
sys.exit(0)
with rasterio.open(filename, sharing=False) as src:
    print(src)
    bandnumber = 1
    print(bandnumber)
    band = rasterio.band(src, bandnumber)
    scale = band.ds.scales[0]
    offset = band.ds.offsets[0]
    print(scale,offset)
    print(band.ds.read()*scale+offset)