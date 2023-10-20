# pylint: skip-file
# This file is part of datacube-ows, part of the Open Data Cube project.
# See https://opendatacube.org for more information.
#
# Copyright (c) 2017-2021 OWS Contributors
# SPDX-License-Identifier: Apache-2.0


# Example configuration file for datacube_ows.
#
# The file was originally the only documentation for the configuration file format.
# Detailed and up-to-date formal documentation is now available and this this file
# is no longer actively maintained and may contain errors or obsolete elements.
#
# https://datacube-ows.readthedocs.io/en/latest/configuration.html

# THIS EXAMPLE FILE
#
# In this example file, there are some reusable code chunks defined at the top.  The actual
# config tree is defined as ows_cfg below the reusable chunks.
#

from layers.analysed_sst import layer as analysed_sst_layer
from layers.sea_ice_fraction import layer as sea_ice_fraction_layer
from layers.sea_ice_fraction_anomaly import layer as sea_ice_fraction_anomaly_layer
from layers.sst_uncertainty import layer as analysed_sst_uncertainty_layer
from layers.oc_chlor_a import layer as chlor_a_layer
from layers.chuk_maxst import layer as maxst_layer
from layers.beta_c4grass import layer as beta_c4grass_layer
from layers.analysed_sst_anomaly import layer as analysed_sst_anomaly_layer

# REUSABLE CONFIG FRAGMENTS - resource limit declarations

# MAIN CONFIGURATION OBJECT

ows_cfg = {
    # Config entries in the "global" section apply to all services and all layers/coverages
    "global": {

        # These HTML headers are added to all responses
        # Optional, default {} - no added headers
        "response_headers": {
            "Access-Control-Allow-Origin": "*",  # CORS header (strongly recommended)
        },
        # Which web service(s) should be implemented by this instance
        # Optional, defaults: wms,wmts: True, wcs: False
        "services": {
            "wms": True,
            "wmts": False,
            "wcs": False
        },
        # Service title - appears e.g. in Terria catalog (required)
        "title": "Open web-services for the Open Data Cube",
        # Service URL.
        # A list of fully qualified URLs that the service can return
        # in the GetCapabilities documents based on the requesting url
        "allowed_urls": ["http://192.171.169.123:5000/"],
        # URL that humans can visit to learn more about the service(s) or organization
        # should be fully qualified
        "info_url": "http://opendatacube.org",
        # Abstract - longer description of the service (Note this text is used for both WM(T)S and WCS)
        # Optional - defaults to empty string.
        "abstract": """This web-service serves georectified raster data from our very own special Open Data Cube instance.""",
        # Keywords included for all services and products
        # Optional - defaults to empty list.
        "keywords": [
            "satellite",
            "australia",
            "time-series",
        ],
        # Contact info.
        # Optional but strongly recommended - defaults to blank.
        "contact_info": {
            "person": "Firstname Surname",
            "organisation": "Acme Corporation",
            "position": "CIO (Chief Imaginary Officer)",
            "address": {
                "type": "postal",
                "address": "GPO Box 999",
                "city": "Metropolis",
                "state": "North Arcadia",
                "postcode": "12345",
                "country": "Elbonia",
            },
            "telephone": "+61 2 1234 5678",
            "fax": "+61 2 1234 6789",
            "email": "test@example.com",
        },
        # Attribution.
        #
        # This provides a way to identify the source of the data used in a WMS layer or layers.
        # This entire section is optional.  If provided, it is taken as the
        # default attribution for any layer that does not override it.
        "attribution": {
            # Attribution must contain at least one of ("title", "url" and "logo")
            # A human readable title for the attribution - e.g. the name of the attributed organisation
            "title": "Acme Satellites",
            # The associated - e.g. URL for the attributed organisation
            "url": "http://www.acme.com/satellites",
            # Logo image - e.g. for the attributed organisation
            "logo": {
                # Image width in pixels (optional)
                "width": 370,
                # Image height in pixels (optional)
                "height": 73,
                # URL for the logo image. (required if logo specified)
                "url": "https://www.acme.com/satellites/images/acme-370x73.png",
                # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                "format": "image/png",
            }
        },
        # If fees are charged for the use of the service, these can be described here in free text.
        # If blank or not included, defaults to "none".
        "fees": "",
        # If there are constraints on access to the service, they can be described here in free text.
        # If blank or not included, defaults to "none".
        "access_constraints": "",
        # Supported co-ordinate reference systems. Any coordinate system supported by GDAL and Proj.4J can be used.
        # At least one CRS must be included.  At least one geographic CRS must be included if WCS is active.
        # WGS-84 (EPSG:4326) is strongly recommended, but not required.
        # Web Mercator (EPSG:3857) is strongly recommended, but is only required if WMTS is active.
        "published_CRSs": {
            "EPSG:3857": {  # Web Mercator
                "geographic": False,
                "horizontal_coord": "x",
                "vertical_coord": "y",
            },
            "EPSG:4326": {  # WGS-84
                "geographic": True,
                "vertical_coord_first": True
            },
            "EPSG:27700": {  # WGS-84
                "geographic": False,
                "vertical_coord_first": True
            }
        },
    },   #### End of "global" section.

    # Config items in the "wms" section apply to the WMS service (and WMTS, which is implemented as a
    # thin wrapper to the WMS code unless stated otherwise) to all WMS/WMTS layers (unless over-ridden).
    "wms": {
        # Provide S3 data URL, bucket name for data_links in GetFeatureinfo responses
        # Note that this feature is currently restricted to data stored in AWS S3.
        # This feature is also fairly specialised to DEA requirements and may not be suited to more general use.
        # All Optional
        # "s3_url": "http://data.au",
        # "s3_bucket": "s3_bucket_name",
        # "s3_aws_zone": "ap-southeast-2",
        # Max tile height/width for wms.  (N.B. Does not apply to WMTS)
        # Optional, defaults to 256x256
        "max_width": 256,
        "max_height": 256,

        # These define the AuthorityURLs.
        # They represent the authorities that define the "Identifiers" defined layer by layer below.
        # The spec allows AuthorityURLs to be defined anywhere on the Layer heirarchy, but datacube_ows treats them
        # as global entities.
        # Required if identifiers are to be declared for any layer.
        "authorities": {
            # The authorities dictionary maps names to authority urls.
            "auth": "https://authoritative-authority.com",
            "idsrus": "https://www.identifiers-r-us.com",
        }
    }, ####  End of "wms" section.

    # Config items in the "wmts" section apply to the WMTS service only.
    # Note that most items in the "wms" section apply to the WMTS service
    # as well as the WMS service.
    #
    # Config items in the "wmts" section apply to all WMTS layers. All
    # entries are optional and the entire section may be omitted.
    "wmts": {
        # Datacube-ows always supports the standard "Google Maps" style
        # EPSG:3857-based tile matrix set.
    },

    # Config items in the "wcs" section apply to the WCS service to all WCS coverages
    # (unless over-ridden).
    "wcs": {
        # Supported WCS formats
        # NetCDF and GeoTIFF work "out of the box".  Other formats will require writing a Python function
        # to do the rendering.
        "formats": {
            # Key is the format name, as used in DescribeCoverage XML
            "GeoTIFF": {
                # Writing your own renderers is not documented.
                "renderers": {
                    "1": "datacube_ows.wcs1_utils.get_tiff",
                    "2": "datacube_ows.wcs2_utils.get_tiff",
                },
                # The MIME type of the image, as used in the Http Response.
                "mime": "image/geotiff",
                # The file extension to add to the filename.
                "extension": "tif",
                # Whether or not the file format supports multiple time slices.
                "multi-time": False
            },
            "netCDF": {
                "renderers": {
                    "1": "datacube_ows.wcs1_utils.get_netcdf",
                    "2": "datacube_ows.wcs2_utils.get_netcdf",
                },
                "mime": "application/x-netcdf",
                "extension": "nc",
                "multi-time": True,
            }
        },
        # The wcs:native_format must be declared in wcs:formats dict above.
        # Maybe over-ridden at the named layer (i.e. coverage)
        # level.
        "native_format": "GeoTIFF",
    }, ###### End of "wcs" section

    # Products published by this datacube_ows instance.
    # The layers section is a list of layer definitions.  Each layer may be either:
    # 1) A folder-layer.  Folder-layers are not named and can contain a list of child layers.  Folder-layers are
    #    only used by WMS and WMTS - WCS does not support a hierarchical index of coverages.
    # 2) A mappable named layer that can be requested in WMS GetMap or WMTS GetTile requests.  A mappable named layer
    #    is also a coverage, that may be requested in WCS DescribeCoverage or WCS GetCoverage requests.
    "layers": [
        {
            # NOTE: This layer is a folder - it is NOT "named layer" that can be selected in GetMap requests
            # Every layer must have a human-readable title
            "title": "Sea Surface Temperature",

            "abstract": "Sea Surface Temperature Layers",
            # NOTE: Folder-layers do not have a layer "name".

            # Keywords are optional, but can be added at any folder level and are cumulative.
            # A layer combines its own keywords, the keywords of it's parent (and grandparent, etc) layers,
            # and any keywords defined in the global section above.
            #
            "keywords": [
                "sst"
            ],

            # Attribution.  This entire section is optional.  If provided, it overrides any
            #               attribution defined in the wms section above or any higher layers, and
            #               applies to this layer and all child layers under this layer unless itself
            #               overridden.
            "attribution": {
                # Attribution must contain at least one of ("title", "url" and "logo")
                # A human readable title for the attribution - e.g. the name of the attributed organisation
                "title": "EOCIS",
                # The associated - e.g. URL for the attributed organisation
                "url": "https://eocis.org",
                # Logo image - e.g. for the attributed organisation
                "logo": {
                    # URL for the logo image. (required if logo specified)
                    "url": "https://eocis.org/wp-content/uploads/2023/06/EOCIS-Logo-Final-1024x451.png",
                    # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                    "format": "image/png",
                }
            },
            # Folder-type layers include a list of sub-layers
            "layers": [
                analysed_sst_layer, sea_ice_fraction_layer, analysed_sst_uncertainty_layer
            ]
        },
        {
            # NOTE: This layer is a folder - it is NOT "named layer" that can be selected in GetMap requests
            # Every layer must have a human-readable title
            "title": "Sea Surface Temperature Anomalies",

            "abstract": "Sea Surface Temperature Anomaly Layers",
            # NOTE: Folder-layers do not have a layer "name".

            # Keywords are optional, but can be added at any folder level and are cumulative.
            # A layer combines its own keywords, the keywords of it's parent (and grandparent, etc) layers,
            # and any keywords defined in the global section above.
            #
            "keywords": [
                "sst"
            ],

            # Attribution.  This entire section is optional.  If provided, it overrides any
            #               attribution defined in the wms section above or any higher layers, and
            #               applies to this layer and all child layers under this layer unless itself
            #               overridden.
            "attribution": {
                # Attribution must contain at least one of ("title", "url" and "logo")
                # A human readable title for the attribution - e.g. the name of the attributed organisation
                "title": "EOCIS",
                # The associated - e.g. URL for the attributed organisation
                "url": "https://eocis.org",
                # Logo image - e.g. for the attributed organisation
                "logo": {
                    # URL for the logo image. (required if logo specified)
                    "url": "https://eocis.org/wp-content/uploads/2023/06/EOCIS-Logo-Final-1024x451.png",
                    # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                    "format": "image/png",
                }
            },
            # Folder-type layers include a list of sub-layers
            "layers": [
                analysed_sst_anomaly_layer, sea_ice_fraction_anomaly_layer
            ]
        },
        {
            # NOTE: This layer is a folder - it is NOT "named layer" that can be selected in GetMap requests
            # Every layer must have a human-readable title
            "title": "Ocean Colour Chlorophyll",

            "abstract": "Ocean Colour Layers",
            # NOTE: Folder-layers do not have a layer "name".

            # Keywords are optional, but can be added at any folder level and are cumulative.
            # A layer combines its own keywords, the keywords of it's parent (and grandparent, etc) layers,
            # and any keywords defined in the global section above.
            #
            "keywords": [
                "ocean colour", "chlorophyll"
            ],

            # Attribution.  This entire section is optional.  If provided, it overrides any
            #               attribution defined in the wms section above or any higher layers, and
            #               applies to this layer and all child layers under this layer unless itself
            #               overridden.
            "attribution": {
                # Attribution must contain at least one of ("title", "url" and "logo")
                # A human readable title for the attribution - e.g. the name of the attributed organisation
                "title": "EOCIS",
                # The associated - e.g. URL for the attributed organisation
                "url": "https://eocis.org",
                # Logo image - e.g. for the attributed organisation
                "logo": {
                    # URL for the logo image. (required if logo specified)
                    "url": "https://eocis.org/wp-content/uploads/2023/06/EOCIS-Logo-Final-1024x451.png",
                    # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                    "format": "image/png",
                }
            },
            # Folder-type layers include a list of sub-layers
            "layers": [
               chlor_a_layer
            ]
        },
        {
            # NOTE: This layer is a folder - it is NOT "named layer" that can be selected in GetMap requests
            # Every layer must have a human-readable title
            "title": "CHUK Max Surface Temperature",

            "abstract": "Max Surface Temperature",
            # NOTE: Folder-layers do not have a layer "name".

            # Keywords are optional, but can be added at any folder level and are cumulative.
            # A layer combines its own keywords, the keywords of it's parent (and grandparent, etc) layers,
            # and any keywords defined in the global section above.
            #
            "keywords": [
                "surface temperature"
            ],

            # Attribution.  This entire section is optional.  If provided, it overrides any
            #               attribution defined in the wms section above or any higher layers, and
            #               applies to this layer and all child layers under this layer unless itself
            #               overridden.
            "attribution": {
                # Attribution must contain at least one of ("title", "url" and "logo")
                # A human readable title for the attribution - e.g. the name of the attributed organisation
                "title": "EOCIS",
                # The associated - e.g. URL for the attributed organisation
                "url": "https://eocis.org",
                # Logo image - e.g. for the attributed organisation
                "logo": {
                    # URL for the logo image. (required if logo specified)
                    "url": "https://eocis.org/wp-content/uploads/2023/06/EOCIS-Logo-Final-1024x451.png",
                    # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                    "format": "image/png",
                }
            },
            # Folder-type layers include a list of sub-layers
            "layers": [
               maxst_layer
            ]
        },
        {
            # NOTE: This layer is a folder - it is NOT "named layer" that can be selected in GetMap requests
            # Every layer must have a human-readable title
            "title": "Soil Moisture",

            "abstract": "Soil Moisture Layers",
            # NOTE: Folder-layers do not have a layer "name".

            # Keywords are optional, but can be added at any folder level and are cumulative.
            # A layer combines its own keywords, the keywords of it's parent (and grandparent, etc) layers,
            # and any keywords defined in the global section above.
            #
            "keywords": [
                "soil moisture"
            ],

            # Attribution.  This entire section is optional.  If provided, it overrides any
            #               attribution defined in the wms section above or any higher layers, and
            #               applies to this layer and all child layers under this layer unless itself
            #               overridden.
            "attribution": {
                # Attribution must contain at least one of ("title", "url" and "logo")
                # A human readable title for the attribution - e.g. the name of the attributed organisation
                "title": "EOCIS",
                # The associated - e.g. URL for the attributed organisation
                "url": "https://eocis.org",
                # Logo image - e.g. for the attributed organisation
                "logo": {
                    # URL for the logo image. (required if logo specified)
                    "url": "https://eocis.org/wp-content/uploads/2023/06/EOCIS-Logo-Final-1024x451.png",
                    # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                    "format": "image/png",
                }
            },
            # Folder-type layers include a list of sub-layers
            "layers": [
                beta_c4grass_layer
            ]
        }
    ]  ##### End of "layers" list.
} #### End of example configuration object
