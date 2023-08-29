import numpy
import xarray as xr

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
    except Exception as ex:
        print(ex)
        raise
    print(obs)
    return obs
