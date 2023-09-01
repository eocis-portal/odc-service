import datetime
from timestore import TimeStore
import os.path
from io import StringIO
import csv

START_YEAR=1980
END_YEAR=2025

from flask import Flask, render_template, request, send_from_directory, abort, make_response, jsonify

class Config:

    # web service configuration
    HOST = "localhost"                              # the host name or IP address that the web service will listen on
    PORT = 50001                                    # the port that the web service will listen on

app = Flask(__name__)

app.config.from_object(Config())


class App:

    variables = {}

    @staticmethod
    def configure(config):
        App.variables = config["variables"]
        for variable in App.variables:
            location = App.variables[variable]["location"]
            min_year = None
            max_year = None
            period = None
            timestores = {}
            for filename in os.listdir(location):
                if not filename.endswith(".ts"):
                    continue
                filepath = os.path.join(location,filename)
                timestore = TimeStore(filepath)
                timestore.open()
                start_year = timestore.get_start_year()
                end_year = timestore.get_end_year()
                if min_year is None or start_year < min_year:
                    min_year = start_year
                if max_year is None or end_year > max_year:
                    max_year = end_year
                timestores[(start_year,end_year)] = filepath
                if period is None:
                    period = timestore.get_period()

            App.variables[variable]["start_year"] = min_year
            App.variables[variable]["end_year"] = max_year
            App.variables[variable]["time_stores"] = timestores
            App.variables[variable]["period"] = period
            print(f"Registering: {variable}: {min_year} - {max_year}")
            for (start_year, end_year) in timestores:
                print(f"\t{start_year} - {end_year}: "+timestores[(start_year,end_year)])

    def __init__(self):
        pass

    @staticmethod
    @app.route("/timeseries/metadata", methods=['GET'])
    def get_metadata():
        o = {}
        for variable in App.variables:
            vo = App.variables[variable]
            o[variable] = {
                "period": vo["period"],
                "name": vo["name"],
                "ylabel": vo["ylabel"]
            }
        response = jsonify(o)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @staticmethod
    def get_timeseries(variable,lat,lon,fromdt=None,todt=None):
        variable_settings = App.variables[variable]
        period = variable_settings["period"]
        if fromdt is None:
            fromdt = datetime.date(App.variables[variable]["start_year"], 1, 1)
        if todt is None:
            todt = datetime.date(App.variables[variable]["end_year"], 12, 31)

        if period == "monthly":
            fromdt = datetime.date(fromdt.year, fromdt.month, 15)
            todt = datetime.date(todt.year, todt.month, 15)

        series = []
        dt = datetime.date(fromdt.year,fromdt.month,fromdt.day)
        current_year = None
        current_series_end_year = None
        current_series = None
        current_series_idx = 0
        while dt <= todt:
            if current_year is None or dt.year > current_year:
                # when moving to a new year, check if we need to load from a new timestore
                current_year = dt.year

                if current_series_end_year is None or current_year > current_series_end_year:
                    current_series = None
                    if variable in App.variables:

                        time_stores = variable_settings["time_stores"]
                        for (start_year,end_year) in time_stores:
                            if start_year <= current_year and end_year >= current_year:
                                path = time_stores[(start_year,end_year)]
                                timestore = TimeStore(path)
                                timestore.open()
                                current_series = timestore.get(lat=lat, lon=lon)
                                current_series_idx = 0
                                current_series_end_year = end_year
                                if "scale" in variable_settings or "offset" in variable_settings:
                                    scale = variable_settings.get("scale", 1.0)
                                    offset = variable_settings.get("offset", 0.0)
                                    current_series = list(map(lambda t: (t[0] * scale + offset if t[0] is not None else None, t[1]), current_series))
                                break

            value = None
            if current_series:
                while current_series_idx < len(current_series) and current_series[current_series_idx][1] < dt:
                    current_series_idx += 1
                if current_series_idx < len(current_series):
                    value = current_series[current_series_idx][0]

            series.append([dt.strftime("%Y-%m-%d"),value])

            if period == "monthly":
                while True:
                    dt += datetime.timedelta(days=1)
                    if dt.day == 15:
                        break
            else:
                dt += datetime.timedelta(days=1)

        return series

    @staticmethod
    @app.route("/timeseries/<string:variable>/<string:latlon>/<string:fromto>/<string:format>",methods=['GET'])
    def fetch(variable,latlon,fromto,format):
        return App.fetch(variable,latlon,fromto,format)


    @staticmethod
    def fetch(variable, latlon, fromto, format):
        (lat,lon) = tuple(latlon.split(":"))
        (lat,lon) = (float(lat),float(lon))
        (fromdt,todt) = tuple(fromto.split(":"))
        if fromdt:
            fromdt = datetime.datetime.strptime(fromdt,"%Y-%m-%d").date()
        else:
            fromdt = None
        if todt:
            todt = datetime.datetime.strptime(todt, "%Y-%m-%d").date()
        else:
            todt = None
        series = App.get_timeseries(variable,lat,lon,fromdt,todt)
        if format == "json":
            response = jsonify(series)
        elif format == "csv":
            of = StringIO()
            writer = csv.writer(of)
            writer.writerow(["Date",variable])
            for (dt,value) in series:
                writer.writerow([dt,value if value is not None else ""])
            response = make_response(of.getvalue())
            response.headers["Content-type"] = "text/csv"
        else:
            raise ValueError("Invalid format: "+format)
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
