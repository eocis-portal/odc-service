
style = {
    "name": "maxst_style",
    "title": "Max Surface Temperature",
    "abstract": "Max Surface Temperature",
    "index_function": {
         "function": "datacube_ows.band_utils.pre_scaled_band",
         "kwargs": {
             "band": "ST",
             "scale": 1,
             "offset": -273.15
         }
    },
    "needed_bands": ["ST"],
    "color_ramp": [
        {
            "value": 17,
            "color": "#0000FF",
            "alpha": 1.0
        },
        {
            "value": 42,
            "color": "#00FF00"
        },
        {
            "value": 58,
            "color": "#FF0000"
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": True,
        "width": 4,    # 400 pixels at default dpi
        "height": 2,
        "title": "Centigrade"
    }
}