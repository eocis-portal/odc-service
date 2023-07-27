

import numpy as np
import xarray as xr
import os
import calendar

class TimeStore:

    FILLVALUE = -32768

    def __init__(self, filepath, year, nj, ni, dtype=np.int16, scale=1.0, offset=0.0, period="daily"):
        self.year = year
        self.filepath = filepath
        self.dtype = dtype
        self.array = None
        self.period = period
        if self.period == "daily":
            self.shape = (12,nj,ni,31)
        else:
            self.shape = (nj,ni,12)
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

    def get_period(self):
        return self.period

    def open(self):
        if not os.path.exists(self.filepath):
            self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="w+", offset=0,
                                   shape=self.shape, order="C")
            self.array[:, :, :, :] = -32768
        else:
            self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="r+", shape=self.shape,
                                   offset=0, order="C")

    def add_day(self, month, day, data):
        self.array[month,:,:,day] = np.where(np.isnan(data), TimeStore.FILLVALUE, np.int16((data-self.offset)/self.scale))

    def add_month(self, month, data):
        self.array[:,:,month] = data

    def get(self, j, i):
        if self.period == "daily":
            values = self.array[:,j,i,:]
        else:
            values = self.array[j,i,:]
        values = np.where(values == -32768, np.nan, values*self.scale + self.offset)
        values = values.flatten()[self.valid_indexes]
        return values.tolist()


    def save(self):
        self.array.flush()

def tsload(ts,frompath):
    for month in sorted(os.listdir(frompath)):
        monthpath = os.path.join(frompath, month)
        for day in sorted(os.listdir(monthpath)):
            daypath = os.path.join(monthpath, day)
            files = [file for file in os.listdir(daypath) if file.endswith(".nc")]
            if len(files) != 1:
                raise Exception("should be one file")
            filepath = os.path.join(daypath, files[0])
            print("adding:" + filepath)
            monthidx = int(month) - 1
            dayidx = int(day) - 1
            ds = xr.open_dataset(filepath)
            sst = ds["analysed_sst"].data
            ts.add_day(monthidx, dayidx, sst)


if __name__ == '__main__':
    ts = TimeStore("/data/esacci_sst/ts2.npy",2021,3600,7200,scale=0.01,offset=273.15)
    ts.open()
    tsload(ts,"/data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1/2021")
    ts.save()
    print(ts.get(600,50))
