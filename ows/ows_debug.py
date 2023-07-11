import numpy


def mask_by_nan(data: "xarray.Dataset", band: str) -> "numpy.NDArray":
    """
    Mask by nan, for bands with floating point data
    """
    print(data)
    return ~numpy.isnan(data[band])