

import numpy as np
import xarray as xr
import os
import calendar

class Compressor:

    FILLVALUE = -32768

    def __init__(self, filepath_in, filepath_out, nj, ni, dtype=np.int16, scale=1.0, offset=0.0):
        self.filepath_in = filepath_in
        self.filepath_out = filepath_out
        self.dtype = dtype
        self.array_in = None
        self.array_out = None
        self.nj = nj
        self.ni = ni
        self.scale = scale
        self.offset = offset

    def run(self):
        self.array_in = np.memmap(filename=self.filepath_in, dtype=self.dtype, mode="r", 
                shape=(12, self.nj, self.ni, 31), offset=0, order="F")
        self.array_out = np.memmap(filename=self.filepath_out, dtype=self.dtype, mode="w+", offset=0,
                                   shape=(12, self.nj, self.ni), order="C")
        for month in range(12):
            print(f"Processing month {month+1}")
            a = self.array_in[month,:,:,:]
            a_decoded = np.where(a == Compressor.FILLVALUE, np.nan, a)
            a_mean = np.nanmean(a_decoded, axis=2)
            a_encoded = np.where(np.isnan(a_mean), Compressor.FILLVALUE, np.int16((a_mean-self.offset)/self.scale))
            self.array_out[month,:,:] = a_encoded

    def save(self):
        self.array_out.flush()


if __name__ == '__main__':
    cs = Compressor("/data/esacci_sst/ts.npy","/data/esacci_sst/ts_monthly.npy",3600,7200,scale=0.01,offset=273.15)
    cs.run()
    cs.save()
