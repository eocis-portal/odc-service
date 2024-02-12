from .styles.aerosol_FM_aod550_style import style as aerosol_FM_aod550_style
from .resource_limits.standard_resource_limits import limits as standard_resource_limits

layer = {

    "title": "Fine Aerosol Optical Depth",
    "abstract": "Estimates the thickness of fine particles and other aerosols in the atmosphere",

    "name": "FM_AOD550_mean",

    "product_name": "aerosol_monthly",

    "default_time": "2023-01-01",
    "time_axis": {
        "time_interval": 1,
        "start_date": "2018-05-01",
        "end_date": "2023-03-31"
    },

    "bands": {"FM_AOD550_mean": []},
    "resource_limits": standard_resource_limits,
    "dynamic": False,
    "native_crs": "EPSG:4326",
    "native_resolution": [1, -1],

    # The image_processing section must be supplied.
    "image_processing": {
        "extent_mask_func": "ows_debug.mask_by_nan",
        "always_fetch_bands": [],
        "fuse_func": None,
        "manual_merge": False,
        "apply_solar_corrections": False,
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
        "features": [
            {
                "url": "http://domain.tld/path/to/page.html",
                "format": "text/html"
            },
            {
                "url": "http://another-domain.tld/path/to/image.png",
                "format": "image/png"
            }
        ],
        "data": [
            {
                "url": "http://abc.xyz/data-link.xml",
                "format": "application/xml"
            }
        ]
    },
    # The feature_info section is optional.
    "feature_info": {
        # Include an additional list of utc dates in the WMS Get Feature Info. Defaults to False.
        # HACK: only used for GSKY non-solar day lookup.
        "include_utc_dates": False
    },
    # Style definitions
    # The "styling" section is required
    "styling": {
        # The default_style is the style used when no style is explicitly given in the
        # request.  If given, it must be the name of a style in the "styles" list. If
        # not explictly defined it defaults to the first style in "styles" list.
        "default_style": "aerosol_FM_aod550_style",
        # The "styles" list must be explicitly supplied, and must contain at least one
        # style.  See reusable style definitions above for more documentation on
        # defining styles.
        "styles": [
            aerosol_FM_aod550_style
        ]
    }
}