# AODN-STAC

## License

All code in ths repo is covered under the [GPL](LICENSE) license unless otherwise stated.
Code is also available under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0).

## Overview

A repository of STAC exploration for AODN.

Currently there are two examples, both relating to Argo aggregated data.

The notebook [create_catalog_from_geonetwork.ipynb](create_catalog_from_geonetwork.ipynb) will create
a STAC Catalog document based on information from Geonetwork.

The notebook [create_item_from_netcdf.ipynb](create_item_from_netcdf.ipynb) will
create a single STAC Item, based on a NetCDF file.

Both of these notebooks are just proof-of-concepts and need to be refactored into
some kind of library, perhaps, or a command line tool.

## What's next?

There's a [Docker Compose](docker-compose.yml) file that provides a postgis and
stac-fastapi server. And there's a [Makefile](Makefile) that demonstrates
the commands to use to populate the DB.

Once the DB has lots of collections and items in it, we can use it as a powerful
search API for all our datasets on S3!
