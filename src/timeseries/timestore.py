

import numpy as np
import xarray as xr
import os
import calendar

class TimeStore:

    FILLVALUE = -32768

    def __init__(self, filepath, year, nj, ni, dtype=np.int16, scale=1.0, offset=0.0):
        self.year = year
        self.filepath = filepath
        self.dtype = dtype
        self.array = None
        self.nj = nj
        self.ni = ni
        self.scale = scale
        self.offset = offset
        self.valid_indexes = []
        for idx in range(12*31):
            month = idx//31
            day = idx - month*31
            (_,nr_days) = calendar.monthrange(self.year,1+month)
            # print(month,nr_days)
            if day < nr_days:
                self.valid_indexes.append(idx)
        print(len(self.valid_indexes))

    def open(self):
        if not os.path.exists(self.filepath):
            self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="w+", offset=0,
                                   shape=(12, self.nj, self.ni, 31), order="F")
            self.array[:, :, :, :] = -32768
        else:
            self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="r+", shape=(12, self.nj, self.ni, 31),
                                   offset=0, order="F")

    def add(self, month, day, data):
        self.array[month,:,:,day] = data

    def get(self, j, i):
        values = self.array[:,j,i,:].flatten().tolist()
        decoded = []
        for idx in self.valid_indexes:
            if values[idx] == TimeStore.FILLVALUE:
                decoded.append(None)
            else:
                decoded.append(values[idx]*self.scale + self.offset)
        return decoded

    def save(self):
        self.array.flush()

def test_load(ts):
    rootpath = "/home/dev/data/regrid/sst/2022"
    for month in sorted(os.listdir(rootpath)):
        monthpath = os.path.join(rootpath, month)
        for day in sorted(os.listdir(monthpath)):
            daypath = os.path.join(monthpath, day)
            files = [file for file in os.listdir(daypath) if file.endswith(".nc")]
            if len(files) != 1:
                raise Exception("should be one file")
            filepath = os.path.join(daypath, files[0])
            print("adding:" + filepath)
            monthidx = int(month) - 1
            dayidx = int(day) - 1
            ds = xr.open_dataset(filepath, mask_and_scale=False)
            sst = ds["analysed_sst"].coarsen(lat=10, lon=10).mean().data
            ts.add(monthidx, dayidx, sst)


if __name__ == '__main__':
    ts = TimeStore("ts.npy",2022,3600,7200,scale=0.01,offset=273.15)
    ts.open()
    test_load(ts)
    print(ts.get(600,50))
