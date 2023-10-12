style = {
    "name": "soil_moisture_style",
    "title": "Soil Moisture",
    "abstract": "Soil Moisture",
    "index_expression": "beta_c4grass",
    "needed_bands": ["beta_c4grass"],
    "color_ramp": [
        {
            "value": 0,
            "color": "#964B00",
            "alpha": 1.0
        },
        {
            "value": 100,
            "color": "#00FF00",
            "alpha": 1.0
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": True,
    }
}