from .styles.soil_moisture_style import style as soil_moisture_style
from .resource_limits.standard_resource_limits import limits as standard_resource_limits

layer = {
    "title": "Soil Moisture",
    "abstract": "Gridbox soil moisture availabilty factor (beta) for C4 grasses",
    "name": "beta_c4grass",
    "product_name": "soil_moisture",
    "default_time": "2021-12-31",
    "time_axis": {
        "time_interval": 1,
        "start_date": "2021-01-01",
        "end_date": "2021-12-31"
    },
    "bands": { "beta_c4grass": [] },
    "resource_limits": standard_resource_limits,
    "dynamic": False,
    "native_crs": "EPSG:4326",
    "native_resolution": [0.25, -0.25],
    "image_processing": {
        "extent_mask_func": "ows_debug.mask_by_nan",
        "always_fetch_bands": [],
        "fuse_func": None,
        "manual_merge": False,
        "apply_solar_corrections": False
    },
    # If the WCS section is not supplied, then this named layer will NOT appear as a WCS
    # coverage (but will still be a layer in WMS and WMTS).
    "wcs": {
        "native_format": "netCDF"
    },
    # Each key of the identifiers dictionary must match a name from the authorities dictionary
    # in the global section.  The values are the identifiers defined for this layer by that
    # authority.
    "identifiers": {
        "auth": "ls8_ard",
        "idsrus": "12345435::0054234::GHW::24356-splunge"
    },
    "urls": {
        "features": [],
        "data": []
    },

    "feature_info": {
        "include_utc_dates": False
    },

    "styling": {
        "default_style": "soil_moisture_style",
        "styles": [
            soil_moisture_style
        ]
    }
}