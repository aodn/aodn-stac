import tempfile
from datetime import datetime

import boto3
import fsspec
import numpy as np
import xarray as xr
from botocore import UNSIGNED
from botocore.config import Config
from pystac import Asset, Collection, Item

import logging
import io


def read_dataset_inmemory(s3_path: str) -> xr.Dataset:
    """Read a NetCDF as an XArray using in-memory data"""
    try:
        with io.BytesIO() as inmemoryfile:
            # Use boto to download a file to memory
            s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
            bucket, key = s3_path.replace("s3://", "").split("/", 1)
            s3.download_fileobj(bucket, key, inmemoryfile)
            inmemoryfile.seek(0)

            return xr.open_dataset(inmemoryfile)
    except ValueError as e:
        print(f"Failed to open the file with error: {e}")
        return None


def read_dataset_download(s3_path: str) -> xr.Dataset:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Download the file to a temporary location using boto3
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        bucket, key = s3_path.replace("s3://", "").split("/", 1)
        local_file = tmpdir + "/" + key.split("/")[-1]
        s3.download_file(bucket, key, local_file)

        return xr.open_dataset(local_file)


def read_dataset_streaming(s3_path: str) -> xr.Dataset:
    """Read a NetCDF as an XArray
    dataset from a S3 path."""
    # FSSpec is being used to read data from S3
    options = dict(
        mode="rb",
        anon=True,
        default_fill_cache=False,
        default_cache_type="none"
    )

    # This is slow... maybe the NetCDF4 library can be used instead
    with fsspec.open(s3_path, **options) as f:
        return xr.open_dataset(f)


def get_extent_geojson(data: xr.Dataset) -> tuple[dict, dict]:
    """Get GeoJSON extent from xarray dataset. Probably will only work for Argo"""
    min_x = float(data.LONGITUDE.min())
    max_x = float(data.LONGITUDE.max())
    min_y = float(data.LATITUDE.min())
    max_y = float(data.LATITUDE.max())

    extent = {
        "type": "Polygon",
        "coordinates": [
            [
                [min_x, min_y],
                [min_x, max_y],
                [max_x, max_y],
                [max_x, min_y],
                [min_x, min_y],
            ]
        ],
    }

    bbox = [min_x, min_y, max_x, max_y]

    return extent, bbox


def np_dt64_to_dt(in_datetime: np.datetime64) -> str:
    """Convert numpy datetime64 to datetime"""
    dt = datetime.fromtimestamp(in_datetime.astype(int) / 1e9)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def create_item_from_netcdf(s3_path: str, collection_file: str) -> Item:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logger.info("Reading dataset from S3")
    data = read_dataset_inmemory(s3_path)
    if data is None:
        logger.error("Failed to read the dataset... skipping")
        return None

    # Load the collection so we have a reference
    logger.info("Loading collection")
    collection = Collection.from_file(collection_file)

    # Geometry stuff
    logger.info("Getting extent")
    extent, bbox = get_extent_geojson(data)

    # This can have anything in it. The start and end dates are required.
    properties = dict(
        start_datetime=np_dt64_to_dt(data.JULD.min()),
        end_datetime=np_dt64_to_dt(data.JULD.max()),
        description=data.attrs["description"],
    )

    # Create the actual item
    logger.info("Creating item")
    item = Item(
        id=s3_path.split("/")[-1].rstrip(".nc"),
        geometry=extent,
        properties=properties,
        bbox=bbox,
        datetime=None,
        collection=collection
    )

    # This should be real... and we should really put it on S3 too
    item.set_self_href(s3_path.replace(".nc", "_stac-item.json"))

    # An asset is the actual data file
    logger.info("Creating asset")
    asset = Asset(
        href=s3_path,
        media_type="application/x-netcdf",
        roles=["data"]
    )
    item.add_asset(s3_path, asset)

    # Validate what we're doing, hopefully it passes!
    logger.info("Validating item")
    item.validate()

    return item
