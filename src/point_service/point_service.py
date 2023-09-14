import datetime
import math
import os.path
import xarray as xr

from flask import Flask, render_template, request, send_from_directory, abort, make_response, jsonify

class Config:

    # web service configuration
    HOST = "localhost"                              # the host name or IP address that the web service will listen on
    PORT = 50003                                    # the port that the web service will listen on

app = Flask(__name__)

app.config.from_object(Config())


class App:

    variables = {}

    @staticmethod
    def configure(config):
        App.variables = config["variables"]
        for variable in App.variables:
            print(f"Registering: {variable} with data located at:")
            location = App.variables[variable]["location"]
            for key in location:
                if key != "default":
                    splits = key.split(":")
                    if len(splits) == 2:
                        from_year = int(splits[0])
                        to_year = int(splits[1])
                        print(f"\t{from_year} - {to_year}: {location[key]}")
                    else:
                        raise Exception("Invalid location key: "+key)
            if "default" in location:
                print(f"\tdefault: {location[key]}")


    def __init__(self):
        pass

    @staticmethod
    @app.route("/service/metadata", methods=['GET'])
    def get_metadata():
        o = {}
        for variable in App.variables:
            vo = App.variables[variable]
            o[variable] = {
                "name": vo["name"],
                "units": vo["units"],
                "label": vo["label"],
                "scale": vo["scale"],
                "offset": vo["offset"]
            }
        response = jsonify(o)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @staticmethod
    def get_value(variable,lat,lon,dt:datetime.datetime=None):
        variable_settings = App.variables[variable]
        location_pattern = ""
        for location_key in variable_settings["location"]:
            if location_key != "default":
                splits = location_key.split(":")
                if len(splits) == 2:
                    from_year = int(splits[0])
                    to_year = int(splits[1])
                    if dt.year >= from_year and dt.year <= to_year:
                        location_pattern = variable_settings["location"][location_key]
                        break

        if location_pattern == "":
            location_pattern = variable_settings["location"]["default"]

        try:
            location_path = location_pattern.format(year=dt.year,month=dt.month,day=dt.day)
        except:
            location_path = location_pattern

        if os.path.exists(location_path):
            ds = xr.open_dataset(location_path)
            variable_name = variable_settings.get("variable_name",variable)
            da = ds[variable_name]

            x_dim = variable_settings.get("x_dim","lon")
            y_dim = variable_settings.get("y_dim", "lat")
            selector = {y_dim:lat,x_dim:lon,"method":"nearest"}

            if dt is not None:
                t_dim = variable_settings.get("t_dim", "time")
                selector[t_dim] = dt.strftime("%Y-%m-%d")

            v = da.sel(**selector).data.tolist()
            if not math.isnan(v):
                if "scale" in variable_settings:
                    v = v * variable_settings["scale"]
                if "offset" in variable_settings:
                    v = v + variable_settings["offset"]
            else:
                v = None
            ds.close()
        else:
            v = None
        return {"value":v, "label":variable_settings["label"], "units":variable_settings["units"]}


    @staticmethod
    @app.route("/service/value/<string:variable>/<string:latlon>/<string:dt>",methods=['GET'])
    def fetch_with_time(variable,latlon,dt):
        (lat, lon) = tuple(latlon.split(":"))
        (lat, lon) = (float(lat), float(lon))
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d")
        value = App.get_value(variable, lat, lon, dt)
        response = jsonify(value)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @staticmethod
    @app.route("/service/value/<string:variable>/<string:latlon>", methods=['GET'])
    def fetch(variable, latlon):
        (lat, lon) = tuple(latlon.split(":"))
        (lat, lon) = (float(lat), float(lon))
        value = App.get_value(variable, lat, lon)
        response = jsonify(value)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route('/<path:path>')
    def send_report(path):
        return send_from_directory('static', path)

if __name__ == '__main__':

    import sys
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--host", default=app.config["HOST"])
    parser.add_argument("--port", type=int, default=app.config["PORT"])
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.loads(f.read())
    App.configure(config)
    app.run(host=args.host,port=args.port)
