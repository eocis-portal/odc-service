import datacube
import matplotlib.pyplot as plt

dc = datacube.Datacube(app="my_analysis",config="/home/dev/.datacube.conf")

print(dc.list_products())

print(dc.list_measurements())

datasets = dc.find_datasets(product="sst")

ds = dc.load(datasets=datasets[0:1],output_crs="epsg:3857",x=())
print(ds.sel())