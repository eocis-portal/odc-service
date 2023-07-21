import datacube
import matplotlib.pyplot as plt

dc = datacube.Datacube(app="my_analysis",config="/home/dev/.datacube_integration.conf")

print(dc.list_products())i

print(dc.list_measurements())

datasets = dc.find_datasets(product="sstx")

ds = dc.load(datasets=datasets)
print(ds)