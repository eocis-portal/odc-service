# mapproxy installation

This mapproxy service will serve OSM WMS imagery in EPSG:27700

# installation

```
conda env create -n mapproxy_env python=3.10
conda activate mapproxy_env
pip install mapproxy
mkdir /path/to/mapproxy_install
cp mapproxy.yaml /path/to/mapproxy_install
cd /path/to/mapproxy_install
# mapproxy-util create -t base-config ./
mapproxy-util serve-develop ./mapproxy.yaml -b localhost:8181
```