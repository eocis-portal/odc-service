path = "/home/dev/data/regrid/sst/2022.ts"

from timeseries.timestore import TimeStore

ts = TimeStore(path)
ts.open()
print(ts.get(0,0,with_dates=True,monthly=True))