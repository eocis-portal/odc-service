path = "/home/dev/Projects/CHUK/EOCIS-AUXILARY-L4-LANDCOVER-MERGED-2023-1000M-fv1.0.nc"

import xarray as xr

ds = xr.open_dataset(path)

da = ds["land_cover"]

flag_meanings = da.attrs["flag_meanings"].split(" ")
flag_values = list(map(lambda x:int(x),list(da.attrs["flag_values"])))

assert(len(flag_values) == len(flag_meanings))

lookup = {}
for (name,value) in zip(flag_meanings,flag_values):
    lookup[str(value)] = name

import json
print(json.dumps(lookup,indent=2))