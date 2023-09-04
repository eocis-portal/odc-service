import datetime
import logging
import os.path
import numpy as np
from timestore import TimeStore
import xarray as xr
import sys


class TimeStoreClimatologyBuilder:

    def __init__(self, ts, input_file_pattern):
        self.ts = ts
        self.input_file_pattern = input_file_pattern
        self.logger = logging.getLogger("TimeStoreClimatologyBuilder")
        shape = self.ts.get_shape()
        self.nj = shape[0]
        self.ni = shape[1]
        self.sums = np.zeros((self.nj, self.ni, 12),dtype=np.float32)
        self.counts = np.zeros((self.nj, self.ni, 12),dtype=np.int32)

    def load(self, start_year, start_month, start_day, end_year, end_month, end_day):
        self.load_daily(start_year, start_month, start_day, end_year, end_month, end_day)
        print(self.counts)
        print(self.sums)


        means = np.where(self.counts>0,self.sums/self.counts,np.nan)
        print(means)
        for moy in range(0,12):
            self.ts.add_climatology(moy,means[:,:,moy])

    def load_daily(self, start_year, start_month, start_day, end_year, end_month, end_day):
        start_dt = datetime.date(start_year,start_month,start_day)
        end_dt = None
        if end_year is not None:
            end_dt = datetime.date(end_year,end_month,end_day)
        dt = start_dt
        while end_dt is None or dt < end_dt:
            self.load_day(dt.year, dt.month, dt.day)
            dt += datetime.timedelta(days=1)

    def load_day(self, year, month, day):
        path = self.input_file_pattern.format(year=year, month=month, day=day)
        if os.path.exists(path):
            self.logger.info(f"Processing {path}")
            ds = xr.open_dataset(path)
            a = ds[ts.variable_name].squeeze().data
            self.counts[:,:,month-1] += np.where(np.isnan(a), 0, 1)
            self.sums[:,:,month-1] += np.where(np.isnan(a), 0, a)



if __name__ == '__main__':
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("timeseries_path")
    parser.add_argument("input_path_pattern")
    parser.add_argument("--start-day", type=int, default=1)
    parser.add_argument("--start-month",type=int,default=1)
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-day", type=int, default=31)
    parser.add_argument("--end-month", type=int, default=12)
    parser.add_argument("--end-year", type=int, default=None)

    args = parser.parse_args()

    ts = TimeStore(args.timeseries_path)
    ts.open()

    logging.info("Opened timestore:")
    logging.info(str(ts))

    if args.start_year < ts.start_year or args.start_year > ts.end_year:
        logging.error("start_year outside timestore range")
        sys.exit(-1)
    if args.end_year:
        if args.end_year < args.start_year:
            logging.error("start_year outside timestore range")
        if args.end_year < ts.start_year or args.end_year > ts.end_year:
            logging.error("end_year outside timestore range")

    builder = TimeStoreClimatologyBuilder(ts, args.input_path_pattern)

    builder.load(args.start_year,args.start_month,args.start_day,args.end_year,args.end_month,args.end_day)
    ts.save()
