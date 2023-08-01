import datetime

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
        self.period = None
        self.array = None
        self.nj = None
        self.ni = None
        self.scale = None
        self.offset = None
        self.valid_indexes = []
        self.valid_dates = []
        self.variable_name = None
        self.variable_metadata = None
        self.shape = None
        self.array_offset = None
        self.lat_min = None
        self.lat_max = None
        self.lon_min = None
        self.lon_max = None

    def create(self, year, period, nj, ni, scale, offset, variable_name, variable_metadata, block_size=4096,
               lat_min=-90, lat_max=90,lon_min=-180,lon_max=180):
        if os.path.exists(self.filepath):
            raise RuntimeError(f"Cannot create timestore, {self.filepath} already exists")
        self.year = year
        self.period = period
        self.nj = nj
        self.ni = ni
        self.scale = scale
        self.offset = offset
        self.variable_name = variable_name
        self.variable_metadata = variable_metadata
        self.lon_min = lon_min
        self.lon_max = lon_max
        self.lat_min = lat_min
        self.lat_max = lat_max

        metadata_dict = {
            "period": self.period,
            "year": self.year,
            "nj": self.nj,
            "ni": self.ni,
            "scale": self.scale,
            "offset": self.offset,
            "variable_name": self.variable_name,
            "variable_metadata": self.variable_metadata,
            "lon_min": self.lon_min,
            "lon_max": self.lon_max,
            "lat_min": self.lat_min,
            "lat_max": self.lat_max
        }

        self.calculate_shape()

        metadata_bytes = json.dumps(metadata_dict).encode("utf-8")
        header_length = 16 + len(metadata_bytes)
        header_blocks = (header_length // block_size) + (1 if header_length % block_size > 0 else 0)
        array_size = sum(self.shape)
        body_blocks = (array_size // block_size) + (1 if array_size % block_size > 0 else 0)
        self.array_offset = header_blocks * block_size

        with open(self.filepath, "wb") as f:
            for idx in range(header_blocks+body_blocks):
                f.write(b'\x00'*block_size)
            f.seek(0)
            f.write(("%08d" % self.array_offset).encode("ascii"))
            f.write(("%08d" % len(metadata_bytes)).encode("ascii"))
            f.write(metadata_bytes)
            
        self.open_array()
        self.array[:, :, :, :] = TimeStore.FILLVALUE
        self.array.flush()

    def open(self):
        with open(self.filepath, "rb") as f:
            f.seek(0)
            try:
                self.array_offset = int(f.read(8).decode("utf-8"))
                metadata_length = int(f.read(8).decode("utf-8"))
                metadata_bytes = f.read(metadata_length)
                metadata_dict = json.loads(metadata_bytes.decode("utf-8"))
                self.year = metadata_dict["year"]
                self.period = metadata_dict["period"]
                self.nj = metadata_dict["nj"]
                self.ni = metadata_dict["ni"]
                self.scale = metadata_dict["scale"]
                self.offset = metadata_dict["offset"]
                self.variable_name = metadata_dict["variable_name"]
                self.variable_metadata = metadata_dict["variable_metadata"]
                self.lon_min = metadata_dict["lon_min"]
                self.lon_max = metadata_dict["lon_max"]
                self.lat_min = metadata_dict["lat_min"]
                self.lat_max = metadata_dict["lat_max"]
            except Exception as ex:
                raise RuntimeError(f"Cannot read metadata from {self.filepath}") from ex

        self.calculate_shape()
        self.open_array()

    def open_array(self):
        self.array = np.memmap(filename=self.filepath, dtype=self.dtype, mode="r+", offset=self.array_offset,
                               shape=self.shape, order="C")

    def summary(self):
        s = f"path:                  {self.filepath}\n"
        s += f"variable_name:         {self.variable_name}\n"
        s += f"offset:                {self.offset}\n"
        s += f"scale:                 {self.scale}\n"
        s += f"shape:                 {self.shape}\n"
        return s

    def calculate_shape(self):
        if self.period == "daily":
            self.shape = (12,self.nj,self.ni,31)
        else:
            self.shape = (self.nj,self.ni,12)

        self.valid_indexes = []
        self.valid_dates = []
        if self.period == "daily":
            for idx in range(12*31):
                month = idx//31
                day = idx - month*31
                (_,nr_days) = calendar.monthrange(self.year,1+month)
                if day < nr_days:
                    self.valid_indexes.append(idx)
                    self.valid_dates.append(datetime.date(self.year,month+1,day+1))
        else:
            for month in range(12):
                self.valid_indexes.append(month)
                self.valid_dates.append(datetime.date(self.year, month+1, 1))

    def get_period(self):
        return self.period

    def add_day(self, month, day, data):
        self.array[month,:,:,day] = np.where(np.isnan(data), TimeStore.FILLVALUE, np.int16((data-self.offset)/self.scale))

    def add_month(self, month, data):
        self.array[:,:,month] = np.where(np.isnan(data), TimeStore.FILLVALUE, np.int16((data-self.offset)/self.scale))

    def get(self, lat, lon, with_dates=False):
        j = round((lat - self.lat_min)/(self.lat_max - self.lat_min) * self.nj)
        i = round((lon - self.lon_min) / (self.lon_max - self.lon_min) * self.ni)
        if self.period == "daily":
            values = self.array[:,j,i,:]
        else:
            values = self.array[j,i,:]
        values = np.where(values == -32768, np.nan, values*self.scale + self.offset)
        values = values.flatten()[self.valid_indexes]
        values = values.tolist()
        if with_dates:
            values = [(value,dt) for (value,dt) in zip(values,self.valid_dates) if not np.isnan(value)]
        else:
            values = list(map(lambda v: v if not np.isnan(v) else None, values))
        return values

    def save(self):
        self.array.flush()


