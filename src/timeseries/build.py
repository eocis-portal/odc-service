import logging
import os.path
from timestore import TimeStore
import xarray as xr

class TimeStoreBuilder:

    def __init__(self, from_folder, variable_name):
        self.from_folder = from_folder
        self.variable_name = variable_name
        self.year = int(os.path.split(from_folder)[-1])

    def get_year(self):
        return self.year

    def load(self, into_timestore):
        for month in sorted(os.listdir(self.from_folder)):
            monthpath = os.path.join(self.from_folder, month)
            for day in sorted(os.listdir(monthpath)):
                daypath = os.path.join(monthpath, day)
                files = [file for file in os.listdir(daypath) if file.endswith(".nc")]
                if len(files) != 1:
                    raise Exception(f"{daypath} contains multiple netcdf4 files, expected only one")
                filepath = os.path.join(daypath, files[0])
                print(filepath)
                logging.info(f"adding: {filepath}")
                monthidx = int(month) - 1
                dayidx = int(day) - 1
                ds = xr.open_dataset(filepath)
                sst = ds[self.variable_name].data
                into_timestore.add(monthidx, dayidx, sst)
                break

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder")
    parser.add_argument("input_variable")
    parser.add_argument("output_file")
    parser.add_argument("--scale",type=float,default=0.01)
    parser.add_argument("--offset",type=float,default=273.15)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    builder = TimeStoreBuilder(args.input_folder, args.input_variable)

    ts = TimeStore(args.output_file,builder.get_year(),3600,7200,scale=args.scale,offset=args.offset)
    ts.open()
    ts.set_metadata({"scale":args.scale, "offset":args.offset})
    builder.load(ts)
    ts.save()
    print(ts.get(600,50))