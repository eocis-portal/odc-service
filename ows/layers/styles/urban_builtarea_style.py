

style = {
    "name": "urban_builtarea_style",
    "title": "UK Urban Built Area",
    "abstract": "UK Urban Built Area",
    "index_expression": "urban_area",
    "needed_bands": ["urban_area"],
    "color_ramp": [
        {
            "value": 0,
            "color": "#FFFFFF",
            "alpha": 0
        },
        {
            "value": 0.001,
            "color": "#FFFFFF",
            "alpha": 1
        },
        {
            "value": 1.0,
            "color": "#000000",
            "alpha": 1
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": False
    }
}