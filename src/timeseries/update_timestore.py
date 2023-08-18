import datetime
import logging
import os.path
import numpy as np
from timestore import TimeStore
import xarray as xr
import sys


class TimeStoreBuilder:

    def __init__(self, ts, input_file_pattern):
        self.ts = ts
        self.input_file_pattern = input_file_pattern
        self.logger = logging.getLogger("TimeStoreBuilder")

    def load(self, start_year, start_month, start_day, end_year, end_month, end_day):
        if ts.period == "daily":
            self.load_daily(start_year, start_month, start_day, end_year, end_month, end_day)
        else:
            self.load_monthly(start_year, start_month, end_year, end_month)

    def load_daily(self, start_year, start_month, start_day, end_year, end_month, end_day):
        start_dt = datetime.date(start_year,start_month,start_day)
        end_dt = None
        if end_year is not None:
            end_dt = datetime.date(end_year,end_month,end_day)
        dt = start_dt
        while end_dt is None or dt < end_dt:
            if not self.load_day(dt.year, dt.month, dt.day):
                break
            dt += datetime.timedelta(days=1)

    def load_day(self, year, month, day):
        path = self.input_file_pattern.format(year=year, month=month, day=day)
        if os.path.exists(path):
            self.logger.info(f"Processing {path}")
            ds = xr.open_dataset(path)
            self.ts.add_day(month - 1, day - 1, ds[ts.variable_name].squeeze().data)
            return True
        return False

    def load_monthly(self, start_year, start_month, end_year, end_month):
        year = start_year
        month = start_month
        while year <= end_year and month <= end_month:
            if not self.load_month(year,month):
                break
            month += 1
            if month > 12:
                month = 1
                year += 1

    def load_month(self, year, month):
        count = 0
        sums = np.zeros((self.ts.nj,self.ts.ni))
        day = 1
        complete = False
        while True:
            try:
                datetime.datetime(year,month,day)
            except ValueError:
                complete=True
                break
            path = self.input_file_pattern.format(year=year,month=month,day=day)
            if os.path.exists(path):
                self.logger.info(f"Processing {path}")
                ds = xr.open_dataset(path)
                count += 1
                sums += ds[ts.variable_name].squeeze().data
                day += 1
            else:
                break
        if count:
            self.ts.add_month(year,month-1,sums/count)
        return complete


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

    builder = TimeStoreBuilder(ts, args.input_path_pattern)

    builder.load(args.start_year,args.start_month,args.start_day,args.end_year,args.end_month,args.end_day)
    ts.save()
