
from timestore import TimeStore
import logging

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("timestore_file")
    parser.add_argument("--lat", type=float, default=None)
    parser.add_argument("--lon", type=float, default=None)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    ts = TimeStore(args.timestore_file)
    ts.open()
    print(ts.summary())

    if args.lat is not None and args.lon is not None:
        print(ts.get(lat=args.lat,lon=args.lon, with_dates=True))