# AODN-STAC

A repository of STAC exploration for AODN.

Currently there are two examples, both relating to Argo aggregated data.

The notebook [create_catalog_from_geonetwork.ipynb](create_catalog_from_geonetwork.ipynb) will create
a STAC Catalog document based on information from Geonetwork.

The notebook [create_item_from_netcdf.ipynb](create_item_from_netcdf.ipynb) will
create a single STAC Item, based on a NetCDF file.

Both of these notebooks are just proof-of-concepts and need to be refactored into
some kind of library, perhaps, or a command line tool.

## What's next?

We need to work out how to load these documents into a STAC API implementation.
