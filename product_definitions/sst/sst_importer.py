import datetime
import os
import uuid

template = """
id: %(id)s
creation_dt: %(creation_date)s
product: { name: sst }
product_type: sst
platform: {code: bbb}
instrument: {name: ccc}
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
    analysed_sst:
      path: %(input_path)s
      layer: "analysed_sst"
    analysed_sst_uncertainty:
      path: %(input_path)s
      layer: "analysed_sst_uncertainty"
    sea_ice_fraction:
      path: %(input_path)s
      layer: "sea_ice_fraction"
lineage:
  source_datasets: {}
"""

def dt_formatter(dt):
    return "'"+dt.strftime("%Y-%m-%dT12:00:00")+"'"

start_date = datetime.date(2022, 1, 31)
end_date = datetime.date(2022, 12, 31)

input_path_template = "%(year)04d/%(month)02d/%(day)02d"
output_path_template = "%(year)04d/sst_dataset_%(month)02d_%(day)02d.yaml"

def generate_dataset_yamls(root_input_folder, root_output_folder, start_date, end_date):

    dt = start_date
    while dt <= end_date:
        input_folder = os.path.join(root_input_folder,
            input_path_template % {"year":dt.year, "month":dt.month, "day":dt.day})
        input_files = os.listdir(input_folder)
        if len(input_files) != 1:
            raise Exception(f"More files than expected (1) in {input_folder}")
        input_path = input_files[0]
        output_path = os.path.join(root_output_folder,
            output_path_template % {"year":dt.year, "month":dt.month, "day":dt.day})
        output_folder = os.path.split(output_path)[0]
        os.makedirs(output_folder,exist_ok=True)
        print(output_path, dt_formatter(dt))
        with open(output_path,"w") as f:
            dt_s = dt_formatter(dt)

            s = template % {
                "id": str(uuid.uuid4()),
                "creation_date": dt_formatter(datetime.datetime.now()),
                "input_path": os.path.join(input_folder,input_path),
                "from_dt": dt_s,
                "center_dt": dt_s,
                "to_dt": dt_s
            }
            f.write(s)
        dt += datetime.timedelta(days=1)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder",default="/data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1/")
    parser.add_argument("--output-folder", default=".")
    parser.add_argument("--start-date", default="2021-01-01")
    parser.add_argument("--end-date", default="2021-12-31")

    args = parser.parse_args()

    start_date = datetime.datetime.strptime(args.start_date,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d")

    generate_dataset_yamls(args.input_folder, args.output_folder, start_date, end_date)
