style = {
    "name": "sea_ice_fraction_anomaly_style",
    "title": "Sea Ice Fraction Anomaly",
    "abstract": "Sea Ice Fraction Anomaly",
    "index_expression": "sea_ice_fraction_anomaly",
    "needed_bands": ["sea_ice_fraction_anomaly"],

    "color_ramp": [
        {
            "value": -1,
            "color": "#0000FF",
            "alpha": 1.0
        },
        {
            "value": 0,
            "color": "#808080",
            "alpha": 1.0
        },
        {
            "value": 1,
            "color": "#FFFFFF",
            "alpha": 1.0
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": True,
    }
}