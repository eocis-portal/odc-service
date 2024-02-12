
import os
import uuid

from datetime import datetime, timezone
from calendar import monthrange

template = """
id: %(id)s
creation_dt: %(creation_date)s
product: { name: oc_monthly }
product_type: oc_monthly
platform: {code: "Orbview-2,Aqua,Envisat,Suomi-NPP, Sentinel-3a, Sentinel-3b"}
instrument: {name: "SeaWiFS,MODIS,MERIS,VIIRS,OLCI"}
format: {name: NetCDFX}
extent:
  coord:
    ll: {lat: -90, lon: -180}
    lr: {lat: -90, lon: 180}
    ul: {lat: 90, lon: -180}
    ur: {lat: 90, lon: 180}
  from_dt: %(from_dt)s
  center_dt: %(center_dt)s
  to_dt: %(to_dt)s
grid_spatial:
  projection:
    geo_ref_points:
      ll: {x: -180, y: -90}
      lr: {x: 180, y: -90}
      ul: {x: -180, y: 90}
      ur: {x: 180, y: 90}
    spatial_reference: "EPSG:4326"
image:
  bands:
    chlor_a:
      path: %(input_path)s
      layer: "chlor_a"
lineage:
  source_datasets: {}
"""

def dt_formatter(dt):
    return "'"+dt.strftime("%Y-%m-%dT12:00:00")+"'"

input_path_template = "%(year)04d/ESACCI-OC-L3S-CHLOR_A-MERGED-1M_MONTHLY_4km_GEO_PML_OCx-%(year)04d%(month)02d-fv6.0.nc"
output_path_template = "%(year)04d_dataset_%(month)02d.yaml"

def generate_dataset_yamls(root_input_folder, root_output_folder, month_ranges):

    for (year,start_month,end_month) in month_ranges:
        for month in range(start_month, end_month+1):
            input_path = os.path.join(root_input_folder,
                input_path_template % {"year":year, "month":month})
            output_path = os.path.join(root_output_folder,
                output_path_template % {"year":year, "month":month})
            output_folder = os.path.split(output_path)[0]
            os.makedirs(output_folder,exist_ok=True)
            if os.path.exists(input_path):
                (_, last_day_in_month) = monthrange(year, month)
                start_time = datetime(year,month,1,0,0,0,tzinfo=timezone.utc)
                mid_time = datetime(year, month, 15,12,0,0,tzinfo=timezone.utc)
                end_time = datetime(year,month,last_day_in_month,23,59,59,tzinfo=timezone.utc)

                print(output_path, dt_formatter(mid_time))
                with open(output_path,"w") as f:
                    s = template % {
                        "id": str(uuid.uuid4()),
                        "creation_date": dt_formatter(datetime.utcnow()),
                        "input_path": input_path,
                        "from_dt": dt_formatter(start_time),
                        "center_dt": dt_formatter(mid_time),
                        "to_dt": dt_formatter(end_time)
                    }
                    f.write(s)


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder",default="/data/ocean_colour_monthly")
    parser.add_argument("--output-folder", default="definitions")

    parser.add_argument("--start-year", type=int, default=1997)
    parser.add_argument("--start-month", type=int, default=9)
    parser.add_argument("--end-year", type=int, default=2022)
    parser.add_argument("--end-month", type=int, default=12)

    args = parser.parse_args()

    month_ranges= []
    for year in range(args.start_year, args.end_year+1):
        start_month = 1 if year > args.start_year else args.start_month
        end_month = 12 if year < args.end_year else args.end_month
        month_ranges.append((year,start_month,end_month))

    generate_dataset_yamls(args.input_folder, args.output_folder, month_ranges)
