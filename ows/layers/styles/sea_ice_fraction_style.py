style = {
    "name": "sea_ice_fraction_style",
    "title": "Sea Ie Fraction",
    "abstract": "Sea Ice Fraction",
    "index_expression": "se_ice_fraction",
    "needed_bands": ["se_ice_fraction"],

    "color_ramp": [
        {
            "value": 0,
            "color": "#0000FF",
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