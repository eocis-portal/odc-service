limits = {
    "wms": {
        # WMS/WMTS resource limits
        #
        # There are two independent resource limits applied to WMS/WMTS requests.  If either
        # limit is exceeded, then either the low-resolution summary product is used if one is defined, otherwise
        # indicative polygon showing the extent of the data is rendered.
        #
        # The fill-colour of the indicative polygons when either wms/wmts resource limits is exceeded.
        # Triplets (rgb) or quadruplets (rgba) of integers 0-255.
        #
        # (The fourth number in an rgba quadruplet represents opacity with 255 being fully opaque and
        # 0 being fully transparent.)
        #
        # Defaults to [150, 180, 200, 160]
        "zoomed_out_fill_colour": [255, 0, 0, 160],

        # WMS/WMTS Resource Limit 1: Min zoom factor
        #
        # The zoom factor is a dimensionless number calculated from the request in a way that is independent
        # of the CRS. A higher zoom factor corresponds to a more zoomed in view.
        #
        # If the zoom factor of the request is less than the minimum zoom factor (i.e. is zoomed out too far)
        # then indicative polygons are rendered instead of accessing the actual data.
        #
        # Defaults to 300.0
        "min_zoom_factor": 0.0,

        # Min zoom factor (above) works well for small-tiled requests, (e.g. 256x256 as sent by Terria).
        # However, for large-tiled requests (e.g. as sent by QGIS), large and intensive queries can still
        # go through to the datacube.
        #
        # max_datasets specifies a maximum number of datasets that a GetMap or GetTile request can retrieve.
        # Indicatative polygons are displayed if a request exceeds the limits imposed by EITHER max_dataset
        # OR min_zoom_factor.
        #
        # max_datasets should be set in conjunction with min_zoom_factor so that Terria style 256x256
        # tiled requests respond consistently - you never want to see a mixture of photographic tiles and polygon
        # tiles at a given zoom level.  i.e. max_datasets should be greater than the number of datasets
        # required for most intensive possible photographic query given the min_zoom_factor.
        # Note that the ideal value may vary from product to product depending on the size of the dataset
        # extents for the product.
        # Defaults to zero, which is interpreted as no dataset limit.
        "max_datasets": 10,
        # Dataset cache rules.
        #
        # The number of datasets accessed by a GetMap/GetTile/GetCoverage query can be used to control
        # the cache-control headers returned by the query.
        #
        # Special cases:
        #
        # 1. No dataset_cache_rules element: Never return a cache-control header
        # 2. dataset_cache_rules set to an empty list []:  Return no-cache for all queries.
        # 3. General case: refer to comments embedded in example below.
        "dataset_cache_rules": []
    },
    "wcs": {
        # wcs::max_datasets is the WCS equivalent of wms::max_datasets.  The main requirement for setting this
        # value is to avoid gateway timeouts on overly large WCS requests (and reduce server load).
        #
        # Defaults to zero, which is interpreted as no dataset limit.
        "max_datasets": 16,
        # dataset_cache_rules can be set independently for WCS requests.  This example omits it, so
        # WCS GetCoverage requests will always return no cache-control header.
    }
}