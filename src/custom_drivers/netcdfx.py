

from datacube.drivers.netcdf.driver import NetcdfReaderDriver, NetcdfWriterDriver
from ._rio_x import RasterDatasetDataSource
PROTOCOL = 'file'
FORMAT = 'NetCDFX'
FORMAT_ANOMALY = 'NetCDFX_anomaly'

class NetcdfReaderDriverX(object):
    def __init__(self):
        print("NetcdfReaderDriverX")
        self.name = 'NetcdfReader'
        self.protocols = [PROTOCOL]
        self.formats = [FORMAT, FORMAT_ANOMALY]

    def supports(self, protocol, fmt):
        return fmt in [FORMAT, FORMAT_ANOMALY]

    def new_datasource(self, band):
        return RasterDatasetDataSource(band)


def reader_driver_init():
    return NetcdfReaderDriverX()

def writer_driver_init():
    return NetcdfWriterDriver()
