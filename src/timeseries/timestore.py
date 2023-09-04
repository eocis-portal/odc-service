import datetime

import numpy as np
import json
import os
import calendar

class TimeStore:

    FILLVALUE = -32768

    def __init__(self, filepath):
        self.filepath = filepath
        self.use_int16 = None
        self.dtype = None
        self.start_year = None
        self.end_year = None
        self.period = None
        self.for_climatology = None
        self.array = None
        self.nj = None
        self.ni = None
        self.scale = None
        self.offset = None
        self.valid_indexes = [] # for daily, a list of valid (idx,datetime)
        self.variable_name = None
        self.variable_metadata = None
        self.shape = None
        self.array_offset = None
        self.lat_min = None
        self.lat_max = None
        self.lon_min = None
        self.lon_max = None

    def create(self, start_year, end_year, period, input_shape, use_int16, scale, offset, variable_name, variable_metadata, block_size=4096,
               lat_min=-90, lat_max=90,lon_min=-180,lon_max=180,for_climatology=False):
        self.use_int16 = use_int16
        self.dtype = np.int16 if self.use_int16 else np.float32


        if os.path.exists(self.filepath):
            raise RuntimeError(f"Cannot create timestore, {self.filepath} already exists")
        if period == "daily" and start_year != end_year:
            raise RuntimeError("Multi-year timestores are not currently supported for daily timeseries")

        self.for_climatology = for_climatology
        self.start_year = start_year
        self.end_year = end_year
        self.period = period
        self.nj = input_shape[0]
        self.ni = input_shape[1]
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
            "start_year": self.start_year,
            "end_year": self.end_year,
            "nj": self.nj,
            "ni": self.ni,
            "scale": self.scale,
            "offset": self.offset,
            "variable_name": self.variable_name,
            "variable_metadata": self.variable_metadata,
            "lon_min": self.lon_min,
            "lon_max": self.lon_max,
            "lat_min": self.lat_min,
            "lat_max": self.lat_max,
            "use_int16": self.use_int16,
            "for_climatology": self.for_climatology
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
        if self.use_int16:
            self.array[...] = TimeStore.FILLVALUE
        else:
            self.array[...] = np.nan
        self.array.flush()

    def open(self):
        with open(self.filepath, "rb") as f:
            f.seek(0)
            try:
                self.array_offset = int(f.read(8).decode("utf-8"))
                metadata_length = int(f.read(8).decode("utf-8"))
                metadata_bytes = f.read(metadata_length)
                metadata_dict = json.loads(metadata_bytes.decode("utf-8"))
                self.use_int16 = metadata_dict.get("use_int16",True)
                self.for_climatology = metadata_dict.get("for_climatology",False)
                self.dtype = np.int16 if self.use_int16 else np.float32
                self.start_year = metadata_dict["start_year"]
                self.end_year = metadata_dict["end_year"]
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
        s += f"period:                {self.period}\n"
        s += f"climatology:           {self.for_climatology}\n"
        s += f"interval:              {self.start_year} - {self.end_year}\n"
        s += f"variable_name:         {self.variable_name}\n"
        s += f"offset:                {self.offset}\n"
        s += f"scale:                 {self.scale}\n"
        s += f"shape:                 {self.shape}\n"
        s += f"use_int16:             {self.use_int16}\n"
        return s

    def calculate_shape(self):
        if self.for_climatology:
            if self.period == "daily":
                self.shape = (self.nj, self.ni, 366)
            else:
                self.shape = (self.nj, self.ni, 12)
        else:
            if self.period == "daily":
                self.shape = (12,self.nj,self.ni,31)
                self.valid_indexes = []
                for idx in range(12 * 31):
                    month = idx // 31
                    day = idx - month * 31
                    (_, nr_days) = calendar.monthrange(self.start_year, 1 + month)
                    if day < nr_days:
                        self.valid_indexes.append((idx, datetime.date(self.start_year, month + 1, day + 1)))

            else:
                duration_years = 1 + self.end_year - self.start_year
                self.shape = (self.nj,self.ni,12,duration_years)
                self.valid_indexes = None

    def get_shape(self):
        return (self.nj, self.ni)

    def get_period(self):
        return self.period

    def get_for_climatology(self):
        return self.for_climatology

    def add_day(self, month, day, data):
        if self.for_climatology:
            raise Exception("Use add_climatology with a climatology timestore")
        if self.duse_int16:
            self.array[month,:,:,day] = np.where(np.isnan(data), TimeStore.FILLVALUE, np.int16((data-self.offset)/self.scale))
        else:
            self.array[month, :, :, day] = data

    def add_month(self, year, month, data):
        if self.for_climatology:
            raise Exception("Use add_climatology with a climatology timestore")
        if self.use_int16:
            self.array[:,:,month,year-self.start_year] = np.where(np.isnan(data), TimeStore.FILLVALUE, np.int16((data-self.offset)/self.scale))
        else:
            self.array[:, :, month, year - self.start_year] = data

    def add_climatology(self, index, data):
        if not self.for_climatology:
            raise Exception("Use add_day with a non-climatology timestore")
        if self.use_int16:
            self.array[:,:,index] = np.where(np.isnan(data), TimeStore.FILLVALUE, np.int16((data-self.offset)/self.scale))
        else:
            self.array[:,:,index] = data

    def get_start_year(self):
        return self.start_year

    def get_end_year(self):
        return self.end_year

    def get(self, lat, lon):
        j = round((lat - self.lat_min)/(self.lat_max - self.lat_min) * self.nj)
        i = round((lon - self.lon_min) / (self.lon_max - self.lon_min) * self.ni)
        nan_to_none = lambda v: None if np.isnan(v) else v
        if self.for_climatology:
            values = self.array[j, i, :]
            if self.use_int16:
                values = np.where(values == TimeStore.FILLVALUE, np.nan, values * self.scale + self.offset)
            values = values.flatten().tolist()
            return [nan_to_none(value) for value in values]  # should not be any missing values, though

        if self.period == "daily":
            values = self.array[:, j, i, :] if not self.for_climatology else self.array[j, i, :]
            if self.use_int16:
                values = np.where(values == TimeStore.FILLVALUE, np.nan, values * self.scale + self.offset)
            values = values.flatten().tolist()
            values = [(nan_to_none(values[idx]),dt) for (idx,dt) in self.valid_indexes]
        else:
            values = []
            for year in range(self.start_year, self.end_year+1):
                year_values = self.array[j, i,:,year-self.start_year]
                if self.use_int16:
                    year_values = np.where(year_values == -32768, np.nan, year_values * self.scale + self.offset)
                year_values = year_values.flatten().tolist()
                year_values = [(nan_to_none(year_values[m]),datetime.date(year,m+1,15)) for m in range(12)]
                values += year_values
        return values

    def save(self):
        self.array.flush()




