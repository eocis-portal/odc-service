

style = {
    "name": "suburban_builtarea_style",
    "title": "UK Suburban Built Area",
    "abstract": "UK Suburban Built Area",
    "index_expression": "suburban_area",
    "needed_bands": ["suburban_area"],
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