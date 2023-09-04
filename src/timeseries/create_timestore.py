import logging
import os.path
from timestore import TimeStore
import xarray as xr

def scan_shape(from_folder, y_dim, x_dim):
    for root, dirs, files in os.walk(from_folder):
        for file in files:
            if file.endswith(".nc"):
                ds = xr.open_dataset(os.path.join(root,file))
                nj = ds.dims[y_dim]
                ni = ds.dims[x_dim]
                return (nj, ni)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder")
    parser.add_argument("input_variable")
    parser.add_argument("output_file")
    parser.add_argument("--use-int16", action="store_true")
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    parser.add_argument("--y-dim", type=str, default="lat")
    parser.add_argument("--x-dim", type=str, default="lon")
    parser.add_argument("--period", type=str, default="monthly")
    parser.add_argument("--for-climatology", action="store_true")
    parser.add_argument("--scale",type=float,default=1)
    parser.add_argument("--offset",type=float,default=0)

    args = parser.parse_args()

    start_year = args.start_year

    logging.basicConfig(level=logging.INFO)

    input_shape = scan_shape(args.input_folder,args.y_dim, args.x_dim)

    ts = TimeStore(args.output_file)

    ts.create(args.start_year,args.end_year,args.period,input_shape,use_int16=args.use_int16,scale=args.scale,offset=args.offset,variable_name=args.input_variable,
              variable_metadata={}, for_climatology=args.for_climatology)

    ts.save()

# /home/dev/miniconda3/envs/xarray/bin/python3 /home/dev/github/odc-service/src/timeseries/create_timestore.py --start-year 2022 --end-year 2022 --x-dim lon --y-dim lat --period daily /home/dev/data/regrid/sst analysed_sst /home/dev/data/regrid/sst/2022.ts