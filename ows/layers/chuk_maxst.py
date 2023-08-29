from .styles.maxst_style import style as maxst_style
from .resource_limits.standard_resource_limits import limits as standard_resource_limits

layer = {
    # NOTE: This layer IS a mappable "named layer" that can be selected in GetMap requests
    # Every layer must have a distinct human-readable title and abstract.
    "title": "CHUK - Max Surface Temperature",
    "abstract": "Estimates max Surface Temperature on the CHUK grid",
    # Mappable layers must have a name - this is the layer name that appears in WMS GetMap
    # or WMTS GetTile requests and the coverage name that appears in WCS
    # DescribeCoverage/GetCoverage requests.
    "name": "chuk_maxst",
    # The ODC product name for the associated data product
    "product_name": "chuk_maxst4326_3",

    "default_time": "2022-01-01",
    "time_axis": {
        "time_interval": 1,
        "start_date": "2019-01-01",
        "end_date": "2022-12-31"
    },

    # Supported bands, mapping native band names to a list of possible aliases.
    # See reusable band alias maps above for documentation.
    "bands": { "ST": [] },
    # Resource limits.
    # See reusable resource limit declarations above for documentation.
    "resource_limits": standard_resource_limits,
    # If "dynamic" is False (the default) the the ranges for the product are cached in memory.
    # Dynamic products slow down the generation of the GetCapabilities document - use sparingly.
    "dynamic": False,
    # The resolution of the time access.  Optional. Allowed values are:
    # * "raw" (the default - data with timestamps to be according to the local solar day)
    # * "day" (daily data with date-resolution time stamps)
    # * "month" (for monthly summary datasets)
    # * "year" (for annual summary datasets)
    # "time_resolution": "solar",
    # The "native" CRS.  (as used for resource management calculations and WCS metadata)
    # (Used for resource management calculations and WCS metadata)
    # Must be in the global "published_CRSs" list.
    # Can be omitted if the product has a single native CRS, as this will be used in preference.
    "native_crs": "EPSG:4326",
    # The native resolution (x,y)
    # (Used for resource management calculations and WCS metadata)
    # This is the number of CRS units (e.g. degrees, metres) per pixel in the horizontal
    # and vertical directions for the native CRS.
    # Can be omitted if the product has a single native resolution, as this will be used in preference.
    # E.g. for EPSG:3577; (25.0,25.0) for Landsat-8 and (10.0,10.0 for Sentinel-2)
    "native_resolution": [0.001, 0.001],

    # The image_processing section must be supplied.
    "image_processing": {
        # Extent mask function
        # Determines what portions of dataset is potentially meaningful data.
        #
        # All the formats described above for "flags->fuse_func" are
        # supported here as well.
        #
        # Additionally, multiple extent mask functions can be specified as a list of any of
        # supported formats.  The result is the intersection of all supplied mask functions.
        #
        # The function is assumed to take two arguments, data (an xarray Dataset) and band (a band name).  (Plus any additional
        # arguments required by the args and kwargs values in format 3, possibly including product_cfg.)
        #
        "extent_mask_func": "ows_debug.mask_by_nan",

        # Bands to always fetch from the Datacube, even if it is not used by the active style.
        # Useful for when a particular band is always needed for the extent_mask_func,
        "always_fetch_bands": [],
        # Fuse func
        #
        # Determines how multiple dataset arrays are compressed into a single time array
        # All the formats described above for "extent_mask_func" are supported here as well.
        # (Passed through to datacube load_data() function.)
        #
        # Defaults to None.
        "fuse_func": None,
        # Set to true if the band product dataset extents include nodata regions.
        # Defaults to False.
        "manual_merge": False,
        # Apply corrections for solar angle, for "Level 1" products.
        # (Defaults to false - should not be used for NBAR/NBAR-T or other Analysis Ready products
        "apply_solar_corrections": False,
    },
    # If the WCS section is not supplied, then this named layer will NOT appear as a WCS
    # coverage (but will still be a layer in WMS and WMTS).
    "wcs": {
        # The native format advertised for the coverage.
        # Must be one of the formats defined
        # in the global wcs formats section.
        # Optional: if not supplied defaults to the
        # globally defined native_format.
        "native_format": "netCDF"
    },
    # Each key of the identifiers dictionary must match a name from the authorities dictionary
    # in the global section.  The values are the identifiers defined for this layer by that
    # authority.
    "identifiers": {
        "auth": "ls8_ard",
        "idsrus": "12345435::0054234::GHW::24356-splunge"
    },
    # The urls section provides the values that are included in the FeatureListURLs and
    # DataURLs sections of a WMS GetCapabilities document.
    # Multiple of each may be defined per product.
    #
    # The entire section the "features and "data" subsections within it are optional. The
    # default is an empty list(s).
    #
    # Each individual entry must include a url and MIME type format.
    #
    # FeatureListURLs point to "a list of the features represented in a Layer".
    # DataURLs "offer a link to the underlying data represented by a particular layer"
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
        "default_style": "maxst_style",
        # The "styles" list must be explicitly supplied, and must contain at least one
        # style.  See reusable style definitions above for more documentation on
        # defining styles.
        "styles": [
            maxst_style
        ]
    }
}