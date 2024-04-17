
colours = "#FF0000 #006600 #732600 #00FF00 #7FE57F #70A800 #998100 #FFFF00 #801A80 #E68CA6 #008073 #D2D2FF #000080 #0000FF #CCB300 #CCB300 #FFFF80 #FFFF80 #8080FF #000000 #808080 #00FFFF".split(" ")

style = {
    "name": "landcover_style",
    "title": "UK Land Cover",
    "abstract": "UK Land Cover",
    "index_expression": "land_cover",
    "needed_bands": ["land_cover"],
    "color_ramp": [
        { "value":idx, "color": colours[idx] } for idx in range(len(colours))
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": False
    }
}