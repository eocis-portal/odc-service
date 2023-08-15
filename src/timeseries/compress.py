

import numpy as np
import xarray as xr
import os
import calendar
import dask

class Compressor:

    FILLVALUE = -32768

    def __init__(self, filepath_in, filepath_out, variable, dtype=np.int16, scale=1.0, offset=0.0):
        self.filepath_in = filepath_in
        self.filepath_out = filepath_out
        self.dtype = dtype
        self.array_in = None
        self.array_out = None
        self.variable = variable
        self.scale = scale
        self.offset = offset

    def run(self):
        ds_in = xr.open_mfdataset(self.filepath_in,chunks={"time": 1})
        print(ds_in)
        return
        drop_vars = []
        for v in ds_in.variables:
            if v not in [self.variable,"time","lat","lon"]:
                drop_vars.append(v)
        # ds_in = ds_in.drop_vars(drop_vars)
        print(ds_in)
        # ds_out = ds_in.groupby('time.month').mean()
        # ds_out.to_netcdf()


if __name__ == '__main__':
    with dask.config.set(**{'array.slicing.split_large_chunks': False}):
        cs = Compressor("/home/dev/data/regrid/sst/2022/01/*/*.nc","/home/dev/data/2022.nc","analysed_sst",scale=0.01,offset=273.15)
        cs.run()

