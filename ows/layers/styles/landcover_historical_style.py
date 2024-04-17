
values = "0 10 11 12 20 30 40 50 60 61 62 70 71 72 80 81 82 90 100 110 120 121 122 130 140 150 151 152 153 160 170 180 190 200 201 202 210 220".split()
colours = "#000000 #ffff64 #ffff64 #ffff00 #aaf0f0 #dcf064 #c8c864 #006400 #00a000 #00a000 #aac800 #003c00 #003c00 #005000 #285000 #285000 #286400 #788200 #8ca000 #be9600 #966400 #966400 #966400 #ffb432 #ffdcd2 #ffebaf #ffc864 #ffd278 #ffebaf #00785a #009678 #00dc82 #c31400 #fff5d7 #dcdcdc #fff5d7 #0046c8 #ffffff".split()
meanings = "no_data cropland_rainfed cropland_rainfed_herbaceous_cover cropland_rainfed_tree_or_shrub_cover cropland_irrigated mosaic_cropland mosaic_natural_vegetation tree_broadleaved_evergreen_closed_to_open tree_broadleaved_deciduous_closed_to_open tree_broadleaved_deciduous_closed tree_broadleaved_deciduous_open tree_needleleaved_evergreen_closed_to_open tree_needleleaved_evergreen_closed tree_needleleaved_evergreen_open tree_needleleaved_deciduous_closed_to_open tree_needleleaved_deciduous_closed tree_needleleaved_deciduous_open tree_mixed mosaic_tree_and_shrub mosaic_herbaceous shrubland shrubland_evergreen shrubland_deciduous grassland lichens_and_mosses sparse_vegetation sparse_tree sparse_shrub sparse_herbaceous tree_cover_flooded_fresh_or_brakish_water tree_cover_flooded_saline_water shrub_or_herbaceous_cover_flooded urban bare_areas bare_areas_consolidated bare_areas_unconsolidated water snow_and_ice".split()

style = {
    "name": "landcover_historical_style",
    "title": "UK Land Cover (Historical)",
    "abstract": "UK Land Cover (Historical)",
    "index_expression": "lccs_class",
    "needed_bands": ["lccs_class"],
    "color_ramp": [
        { "value":int(values[idx]), "color": colours[idx] } for idx in range(len(colours))
    ],
    "include_in_feature_info": True,
    "legend": {
        "show_legend": False
    }
}

if __name__ == '__main__':
    print(len(colours))
    print(len(values))
    print(len(meanings))