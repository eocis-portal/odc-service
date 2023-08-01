import datetime
from timestore import TimeStore
import os.path
from io import StringIO
import csv

from flask import Flask, render_template, request, send_from_directory, abort, make_response, jsonify

class Config:

    # web service configuration
    HOST = "localhost"                              # the host name or IP address that the web service will listen on
    PORT = 50001                                    # the port that the web service will listen on

app = Flask(__name__)

app.config.from_object(Config())


class App:

    locations = {}

    def __init__(self):
        pass

    @staticmethod
    def get_timeseries(variable,lat,lon,fromdt,todt):
        series = []
        dt = datetime.date(fromdt.year,fromdt.month,fromdt.day)
        current_year = None
        current_series = None
        current_series_idx = 0
        while dt <= todt:
            if current_year is None or dt.year != current_year:
                current_year = dt.year
                current_series = None
                current_series_idx = 0
                if variable in App.patterns:
                    pattern = App.patterns[variable]
                    path = pattern % (current_year)
                    if os.path.exists(path):
                        timestore = TimeStore(path)
                        timestore.open()
                        current_series = timestore.get(lat=lat,lon=lon,with_dates=True)
                        current_series_idx = 0

            value = None
            if current_series:
                while current_series_idx < len(current_series) and current_series[current_series_idx][1] != dt:
                    current_series_idx += 1
                if current_series_idx < len(current_series):
                    value = current_series[current_series_idx][0]

            series.append([dt.strftime("%Y-%m-%d"),value])
            dt += datetime.timedelta(days=1)

        return series


    @staticmethod
    @app.route("/timeseries/<string:variable>/<string:latlon>/<string:fromto>/<string:format>",methods=['GET'])
    def test(variable,latlon,fromto,format):
        (lat,lon) = tuple(latlon.split(":"))
        (lat,lon) = (float(lat),float(lon))
        (fromdt,todt) = tuple(fromto.split(":"))
        fromdt = datetime.datetime.strptime(fromdt,"%Y-%m-%d").date()
        todt = datetime.datetime.strptime(todt, "%Y-%m-%d").date()
        series = App.get_timeseries(variable,lat,lon,fromdt,todt)
        if format == "json":
            return jsonify(series)
        elif format == "csv":
            of = StringIO()
            writer = csv.writer(of)
            writer.writerow(["Date",variable])
            for (dt,value) in series:
                writer.writerow([dt,value if value is not None else ""])
            output = make_response(of.getvalue())
            output.headers["Content-type"] = "text/csv"
            return output

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

    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.loads(f.read())
    app.locations = config["locations"]
    app.run(host=args.host,port=args.port)
