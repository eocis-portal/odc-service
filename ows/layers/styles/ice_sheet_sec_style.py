
style = {
    "name": "ice_sheet_sec_style",
    "title": "Surface elevation Change - Ice Sheets",
    "abstract": "Surface elevation Change - Ice Sheets",
    "index_expression": "sec",
    "needed_bands": ["sec"],
    "color_ramp": [
        {
            "value": -3,
            "color": "#FF0000"
        },
        {
            "value": 0,
            "color": "#FFFFFF"
        },
        {
            "value": 3,
            "color": "#0000FF"
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": True,
        "width": 4,    # 400 pixels at default dpi
        "height": 2,
        "title": "metres/year"
    }
}