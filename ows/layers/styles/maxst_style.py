
style = {
    "name": "maxst_style",
    "title": "Max Surface Temperature",
    "abstract": "Max Surface Temperature",
    "index_expression": "ST",
    "needed_bands": ["ST"],
    "color_ramp": [
        {
            "value": 280,
            "color": "#000000",
            "alpha": 1.0
        },
        {
            "value": 350,
            "color": "#FF0000"
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": True,
        "width": 4,    # 400 pixels at default dpi
        "height": 2,
        "title": "Kelvin"
    }
}