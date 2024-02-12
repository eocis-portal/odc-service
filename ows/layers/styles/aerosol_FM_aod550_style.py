style = {
    "name": "aerosol_FM_aod550_style",
    "title": "Aerosol",
    "abstract": "Aerosol",
    "index_expression": "FM_AOD550_mean",
    "needed_bands": ["FM_AOD550_mean"],
    "color_ramp": [
        {
            "value": 0,
            "color": "#FFFFFF",
            "alpha": 1.0
        },
        {
            "value": 1,
            "color": "#FF0000"
        }
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": True,
        "width": 4,    # 400 pixels at default dpi
        "height": 2,
        "title": "AOD thickness"
    }
}