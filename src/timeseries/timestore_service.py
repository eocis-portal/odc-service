import datetime

from flask import Flask, render_template, request, send_from_directory, abort, jsonify

class Config:

    # web service configuration
    HOST = "localhost"                              # the host name or IP address that the web service will listen on
    PORT = 50001                                    # the port that the web service will listen on

app = Flask(__name__)

app.config.from_object(Config())


class App:

    pattern = "/home/dev/data/{YEAR}.npy"

    def __init__(self):
        pass

    @staticmethod
    def get_timeseries(lat,lon,fromdt,todt):
        series = []
        dt = datetime.date(fromdt.year,fromdt.month,fromdt.day)
        while dt <= todt:
            series.append(dt.strftime("%Y-%m-%d"))
            dt += datetime.timedelta(days=1)
        return series


    @staticmethod
    @app.route("/timeseries/<string:latlon>/<string:fromto>",methods=['GET'])
    def test(latlon,fromto):
        (lat,lon) = tuple(latlon.split(":"))
        (lat,lon) = (float(lat),float(lon))
        (fromdt,todt) = tuple(fromto.split(":"))
        fromdt = datetime.datetime.strptime(fromdt,"%Y-%m-%d").date()
        todt = datetime.datetime.strptime(todt, "%Y-%m-%d").date()
        series = App.get_timeseries(lat,lon,fromdt,todt)
        return jsonify(series)

if __name__ == '__main__':
    app.run(host=app.config["HOST"],port=app.config["PORT"])
