import numpy


def mask_by_nan(data: "xarray.Dataset", band: str) -> "numpy.NDArray":
    """
    Mask by nan, for bands with floating point data
    """
    print(data)
    return ~numpy.isnan(data[band])

def pre_scaled_band(data, band, scale, offset):
    # Pre-scale a band as `data[band] * scale + offset`
    return data[band] * scale + offset
