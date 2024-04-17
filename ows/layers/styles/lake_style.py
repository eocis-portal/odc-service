style = {
    "name": "lake_style",
    "title": "UK Lake Locations",
    "abstract": "UK Lake Locations",
    "index_expression": "lake_mask",
    "needed_bands": ["lake_mask"],
    "color_ramp": [
        {
            "value": 0,
            "color": "#000000",
            "alpha": 0
        },
        {
            "value": 1.0,
            "color": "#0000FF",
            "alpha": 1
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": False
    }
}