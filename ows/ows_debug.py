import numpy
import xarray as xr


clim = xr.open_mfdataset("/data/esacci_sst/public/CDR2.1_release/Climatology/L4/v2.1/*.nc")

def mask_by_nan(data: "xarray.Dataset", band: str) -> "numpy.NDArray":
    """
    Mask by nan, for bands with floating point data
    """
    return ~numpy.isnan(data[band])

def pre_scaled_band(data, band, scale, offset):
    print("pre_scaled_band")
    try:
        # Pre-scale a band as `data[band] * scale + offset`
        # return data[band] * scale + offset
        obs =  (data[band] * scale + offset)
        anoms = obs - clim.isel(time=obs.time[0].dt.dayofyear.data-1).squeeze()[band]
    except Exception as ex:
        print(ex)
        raise
    print(obs)
    return obs
