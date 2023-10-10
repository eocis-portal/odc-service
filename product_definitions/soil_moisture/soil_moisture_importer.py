import datetime
import os
import uuid

template = """
id: %(id)s
creation_dt: %(creation_date)s
product: { name: soil_moisture }
product_type: soil_moisture
platform: {code: bbb}
instrument: {name: ccc}
format: {name: NetCDFX}
extent:
  coord:
    ll: {lat: -35.375, lon: -17.875}
    lr: {lat:  -35.375, lon: 51.375}
    ul: {lat: 37.375, lon: -17.875}
    ur: {lat: 37.375, lon: 51.375}
  from_dt: %(from_dt)s
  center_dt: %(center_dt)s
  to_dt: %(to_dt)s
grid_spatial:
  projection:
    geo_ref_points:
      ll: {x: -17.875, y: -35.375}
      lr: {x: 51.375, y: -35.375}
      ul: {x: -17.875, y: 37.375}
      ur: {x: 51.375, y: 37.375}
    spatial_reference: "EPSG:4326"
image:
  bands:
    beta_c4grass:
      path: %(input_path)s
      layer: "beta_c4grass"
lineage:
  source_datasets: {}
"""

def dt_formatter(dt):
    return "'"+dt.strftime("%Y-%m-%dT12:00:00")+"'"

input_path_template = "daily/%(year)04d/%(month)02d/sm%(year)04d_%(month)02d_%(day)02d.v1.0.2.nc"
output_path_template = "%(year)04d/sm_dataset_%(month)02d_%(day)02d.yaml"

def generate_dataset_yamls(root_input_folder, root_output_folder, start_date, end_date):

    dt = start_date
    while dt <= end_date:
        input_path = os.path.join(root_input_folder,
            input_path_template % {"year":dt.year, "month":dt.month, "day":dt.day})
        if not os.path.exists(input_path):
            print(f"Input data filer {input_path} missing, stopping...")
            break
        output_path = os.path.join(root_output_folder,
            output_path_template % {"year":dt.year, "month":dt.month, "day":dt.day})
        if os.path.exists(output_path):
            print(f"{output_path} already exists")
            dt += datetime.timedelta(days=1)
            continue
        output_folder = os.path.split(output_path)[0]
        os.makedirs(output_folder,exist_ok=True)
        print(output_path, dt_formatter(dt))
        with open(output_path,"w") as f:
            dt_s = dt_formatter(dt)
            s = template % {
                "id": str(uuid.uuid4()),
                "creation_date": dt_formatter(datetime.datetime.now()),
                "input_path": input_path,
                "from_dt": dt_s,
                "center_dt": dt_s,
                "to_dt": dt_s
            }
            f.write(s)
        dt += datetime.timedelta(days=1)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder",default="/data/soil_moisture")
    parser.add_argument("--output-folder", default=".")
    parser.add_argument("--start-date", default="1983-01-01")
    parser.add_argument("--end-date", default="2022-12-31")

    args = parser.parse_args()

    start_date = datetime.datetime.strptime(args.start_date,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d")

    generate_dataset_yamls(args.input_folder, args.output_folder, start_date, end_date)
