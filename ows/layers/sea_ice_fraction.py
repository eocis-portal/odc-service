from .styles.sea_ice_fraction_style import style as sea_ice_fraction_style
from .resource_limits.standard_resource_limits import limits as standard_resource_limits

layer = {
    "title": "Se Ice Fraction",
    "abstract": "Estimate of Sea Ice Fraction",
    "name": "sea_ice_fraction",
    "product_name": "sst",
    "default_time": "2021-01-01",
    "time_axis": {
        "time_interval": 1,
        "start_date": "2021-01-01",
        "end_date": "2021-12-31"
    },
    "bands": { "sea_ice_fraction": [] },
    "resource_limits": standard_resource_limits,
    "dynamic": False,
    "native_crs": "EPSG:4326",
    "native_resolution": [0.05, -0.05],
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
        "default_style": "sea_ice_fraction_style",
        "styles": [
            sea_ice_fraction_style
        ]
    }
}