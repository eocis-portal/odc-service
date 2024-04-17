import os
import uuid

from datetime import datetime, timezone

template = """
id: %(id)s
creation_dt: %(creation_date)s
product: { name: chuk_landcover_historical }
product_type: chuk_landcover_historical
platform: {code: bbb}
instrument: {name: ccc}
format: {name: NetCDFX}
extent:
  coord:
    ll: {lat: 47.01322552502985, lon: -16.7980635849523}
    lr: {lat: 47.01322552502985, lon: 5.659063256444921}
    ul: {lat: 61.71634739697962, lon: -16.7980635849523}
    ur: {lat: 61.71634739697962, lon: 5.659063256444921}
  from_dt: %(from_dt)s
  center_dt: %(center_dt)s
  to_dt: %(to_dt)s
grid_spatial:
  projection:
    geo_ref_points:
      ll: { x: -332000, y: -267000 }
      lr: { x: 765000, y: -267000 }
      ul: { x: -332000, y: 1250000 }
      ur: { x: 765000, y: 1250000 }
    spatial_reference: "EPSG:27700"
image:
  bands:
    lccs_class:
      path: %(input_path)s
      layer: lccs_class
lineage:
  source_datasets: {}
"""

def dt_formatter(dt):
    return "'"+dt.strftime("%Y-%m-%dT12:00:00")+"'"

input_path_template = "d1.9-historical_land_cover-%(year)04d.nc"
output_path_template = "%(year)04d_dataset.yaml"

def generate_dataset_yamls(root_input_folder, root_output_folder, start_year, end_year):
    for year in range(start_year, end_year+1):

        input_path = os.path.join(root_input_folder,
            input_path_template % {"year":year})
        output_path = os.path.join(root_output_folder,
            output_path_template % {"year":year})
        output_folder = os.path.split(output_path)[0]
        os.makedirs(output_folder,exist_ok=True)
        if os.path.exists(input_path):

            start_time = datetime(year,1,1,0,0,0,tzinfo=timezone.utc)
            mid_time = datetime(year, 7, 1,12,0,0,tzinfo=timezone.utc)
            end_time = datetime(year,12,31,23,59,59,tzinfo=timezone.utc)

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
    parser.add_argument("--input-folder",default="/data/chuk")
    parser.add_argument("--output-folder", default="definitions")

    parser.add_argument("--start-year", type=int, default=2001)
    parser.add_argument("--end-year", type=int, default=2020)

    args = parser.parse_args()

    generate_dataset_yamls(args.input_folder, args.output_folder, args.start_year, args.end_year)
