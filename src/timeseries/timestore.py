

import numpy as np
import xarray as xr
import json
import os
import calendar

class TimeStore:

    FILLVALUE = -32768

    def __init__(self, filepath):
        self.filepath = filepath
        self.dtype = np.int16
        self.year = None
        self.array = None
        self.nj = None
        self.ni = None
        self.scale = None
        self.offset = None
        self.valid_indexes = []
        self.offset = None
        self.variable_name = None
        self.variable_metadata = None


    def create(self, year, nj, ni, scale, offset, variable_name, variable_metadata):
        self.year = year
        self.period = period
        if self.period == "daily":
            self.shape = (12,nj,ni,31)
        else:
            self.shape = (nj,ni,12)
        self.nj = nj
        self.ni = ni
        self.scale = scale
        self.offset = offset
        self.variable_name = variable_name
        self.variable_metadata = variable_metadata

        metadata_dict = {
            "year": self.year,
            "nj": self.nj,
            "ni": self.ni,
            "scale": self.scale,
            "offset": self.offset,
            "variable_name": self.variable_name,
            "variable_metadata": self.variable_metadata
        }
        metadata_bytes = json.dumps(metadata_dict).encode("utf-8")
        length = len(metadata_bytes)
        blocks = (5+length // 4096)
        self.offset = (blocks+1) * 4096
        with open(self.filepath, "rb+") as f:
            f.seek(0)
            f.write(("%05d" % length).encode("ascii"))
            f.write(metadata_bytes)
            
        self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="w+", offset=self.offset,
                               shape=(12, self.nj, self.ni, 31), order="F")
        self.array[:, :, :, :] = -32768
        self.array.flush()



    def open(self):
            self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="r+", shape=(12, self.nj, self.ni, 31),
                                   offset=self.offset, order="F")

    def index(self):
        for idx in range(12*31):
            month = idx//31
            day = idx - month*31
            (_,nr_days) = calendar.monthrange(self.year,1+month)
            # print(month,nr_days)
            if day < nr_days:
                self.valid_indexes.append(idx)
        print(len(self.valid_indexes))


    def get_metadata(self):
        with open(self.filepath,"rb") as f:
            f.seek(0)
            try:
                length = int(f.read(5).decode("utf-8"))
                metadata_bytes = f.read(length)
                return json.loads(metadata_bytes.decode("utf-8"))
            except:
                print("No metadata?")
                return None


    def add(self, month, day, data):
        self.array[month,:,:,day] = np.where(np.isnan(data),-32768,np.int16(data-self.offset/self.scale))

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


