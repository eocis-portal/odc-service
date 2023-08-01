
style = {
    "name": "sst_style",
    "title": "Sea Surface Temperature",
    "abstract": "Sea Surface Temperature",
    # The index function is continuous value from which the heat map is derived.
    #
    # Two formats are supported:
    # 1. A string containing a fully qualified path to a python function
    #    e.g. "index_function": "datacube_ows.ogc_utils.not_a_real_function_name",
    #
    # 2. A dict containing the following elements:
    #    a) "function" (required): A string containing the fully qualified path to a python function
    #    b) "args" (optional): An array of additional positional arguments that will always be passed to the function.
    #    c) "kwargs" (optional): An array of additional keyword arguments that will always be passed to the function.
    #    d) "mapped_bands" (optional): Boolean (defaults to False). If true, a band mapping function is passed
    #       to the function as a keyword argument named "band_mapper".  This is useful if you are passing band aliases
    #       to the function in the args or kwargs.  The band_mapper allows the index function to convert band aliases to
    #       to band names.
    #
    # The function is assumed to take one arguments, an xarray Dataset.  (Plus any additional
    # arguments required by the args and kwargs values in format 3, possibly including product_cfg.)
    #
    "index_expression": "analysed_sst",
    # "index_function": {
    #     "function": "datacube_ows.band_utils.pre_scaled_band",
    #     "kwargs": {
    #         "band": "analysed_sst",
    #         "scale": 1,
    #         "offset": 0
    #     }
    # },
    # List of bands used by this style. The band may not be passed to the index function if it is not declared
    # here, resulting in an error.  Band aliases can be used here.
    "needed_bands": ["analysed_sst"],
    # The color ramp. Values between specified entries have both their alphas and colours
    # interpolated.
    "color_ramp": [
        # Any value less than the first entry will have colour and alpha of the first entry.
        # (i.e. in this example all negative values will be fully transparent (alpha=0.0).)
        {
            "value": -270,
            "color": "#0000FF",
            "alpha": 0.0
        },
        {
            "value": 270,
            "color": "#0000FF",
            "alpha": 1.0
        },
        {
            "value": 315.0,
            "color": "#FF0000"
        }
    ],
    # If true, the calculated index value for the pixel will be included in GetFeatureInfo responses.
    # Defaults to True.
    "include_in_feature_info": True,
    # Legend section is optional for non-linear colour-ramped styles.
    # If not supplied, a legend for the style will be automatically generated from the colour ramp.
    "legend": {
        # Whether or not to display a legend for this style.
        # Defaults to True for non-linear colour-ramped styles.
        "show_legend": True,
        # Instead of using the generated color ramp legend for the style, a URL to an PNG file can
        # be used instead.  If 'url' is not supplied, the generated legend is used.
        # "url": "http://example.com/custom_style_image.png"
    }
}