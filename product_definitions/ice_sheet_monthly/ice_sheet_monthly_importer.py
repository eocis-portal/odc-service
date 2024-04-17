
import os
import uuid
import xarray as xr

from datetime import datetime, timezone, timedelta
from calendar import monthrange

template = """
id: %(id)s
creation_dt: %(creation_date)s
product: { name: ice_sheet_monthly }
product_type: ice_sheet_monthly
platform: {code: "ESA Radar altimeters: ERS-1, ERS-2, Envisat, CryoSat-2, Sentinel-3A and Sentinel-3B"}
instrument: {name: "ESA Radar altimeters: ERS-1, ERS-2, Envisat, CryoSat-2, Sentinel-3A and Sentinel-3B"}
format: {name: NetCDFX}
extent:
  coord:
    ll: {lat: -90, lon: -180}
    lr: {lat: -90, lon: 180}
    ul: {lat: -57.7, lon: -180}
    ur: {lat: -57.7, lon: 180}
  from_dt: %(from_dt)s
  center_dt: %(center_dt)s
  to_dt: %(to_dt)s
grid_spatial:
  projection:
    geo_ref_points:
      ll: {x: -2600000, y: -2200000}
      lr: {x: 2800000, y: -2200000}
      ul: {x: -2600000, y: 2300000}
      ur: {x: 2800000, y: 2300000}
    spatial_reference: "EPSG:3031"
image:
  bands:
    sec:
      path: %(input_path)s
      layer: "sec"
lineage:
  source_datasets: {}
"""

def dt_formatter(dt):
    return "'"+dt.strftime("%Y-%m-%dT12:00:00")+"'"


output_path_template = "%(year)04d_dataset_%(month)02d_%(day)02d.yaml"

def generate_dataset_yamls(root_input_folder, root_output_folder):

    for filename in os.listdir(root_input_folder):
        input_path = os.path.join(root_input_folder, filename)
        year = int(filename[0:4])
        month = int(filename[4:6])
        day = int(filename[6:8])

        output_path = os.path.join(root_output_folder, output_path_template%{"year":year,"month":month,"day":day})

        mid_time = datetime(year, month, day,12,0,0,tzinfo=timezone.utc)
        start_time = mid_time - timedelta(days=10)
        end_time = mid_time + timedelta(days=10)

        print(output_path, dt_formatter(start_time))

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
    parser.add_argument("--input-folder",default="/data/ice_sheet")
    parser.add_argument("--output-folder", default="definitions")

    args = parser.parse_args()
    os.makedirs(args.output_folder, exist_ok=True)
    generate_dataset_yamls(args.input_folder, args.output_folder)
