import datetime
import os
import uuid

template = """
id: %(id)s
creation_dt: %(creation_date)s
product: { name: oc }
product_type: oc
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
    chlor_a:
      path: %(input_path)s
      layer: "chlor_a"
lineage:
  source_datasets: {}
"""

def dt_formatter(dt):
    return "'"+dt.strftime("%Y-%m-%dT12:00:00")+"'"

start_date = datetime.date(2022, 1, 31)
end_date = datetime.date(2022, 12, 31)

input_path_template = "%(year)04d/EOCIS-OC-L3S-CHLOR_A-MERGED-1D_DAILY_0.05deg_GEO_PML_OCx-%(year)04d%(month)02d%(day)02d-fv6.0.nc"
output_path_template = "%(year)04d/dataset_%(month)02d_%(day)02d.yaml"

def generate_dataset_yamls(root_input_folder, root_output_folder, start_date, end_date):

    dt = start_date
    while dt <= end_date:
        input_path = os.path.join(root_input_folder,
            input_path_template % {"year":dt.year, "month":dt.month, "day":dt.day})
        output_path = os.path.join(root_output_folder,
            output_path_template % {"year":dt.year, "month":dt.month, "day":dt.day})
        output_folder = os.path.split(output_path)[0]
        os.makedirs(output_folder,exist_ok=True)
        if os.path.exists(input_path):
            # some days are missing, only create odc datasets where the files exist
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
    parser.add_argument("--input-folder",default="/data/ocean_colour")
    parser.add_argument("--output-folder", default=".")
    parser.add_argument("--start-date", default="1997-09-04")
    parser.add_argument("--end-date", default="2021-12-31")

    args = parser.parse_args()

    start_date = datetime.datetime.strptime(args.start_date,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d")

    generate_dataset_yamls(args.input_folder, args.output_folder, start_date, end_date)
