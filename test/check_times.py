
import sys

product = sys.argv[1]
import datacube
import datetime

dc = datacube.Datacube(app="my_analysis",config="/home/dev/.datacube.conf")

datasets = dc.find_datasets(product=product)

times = sorted([ds.time.begin for ds in datasets])
start_time = times[0]
end_time = times[-1]
print("checking between:",start_time,end_time)

dt = start_time
index = 0

missing = set()
included = set()

while dt < end_time:
    included.add(dt.year)
    index += 1
    dt += datetime.timedelta(days=1)
    while times[index].date() > dt.date():
        missing.add(dt.year)
        dt += datetime.timedelta(days=1)

print("included years:"+str(included))
print("missing years:"+str(missing))

# included years:{2016, 2017, 2018, 2019, 2021, 2022, 2014, 2010, 2011, 2012, 2013, 1982, 2015}
# missing years:{1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2020}


