import os
import zipfile
from pathlib import Path

import requests
import xarray as xr

# Define the path to the cached ZIP file
cached_file_path = "./cached_data/cloud_mask_warmpool.zip"
zenodo_url = (
    "https://zenodo.org/record/8413762/files/cloud_mask_warmpool.zip?download=1"
)

# Check if the cached file exists
if not os.path.exists(cached_file_path):
    # Download from Zenodo if the cached file doesn't exist
    response = requests.get(zenodo_url, stream=True)
    os.makedirs(os.path.dirname(cached_file_path), exist_ok=True)

    with open(cached_file_path, "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)

with zipfile.ZipFile(cached_file_path, "r") as zip_ref:
    names = zip_ref.namelist()
    zarr_root = names[0]
    if not os.path.exists("dataset_folder"):
        os.makedirs("dataset_folder")
        zip_ref.extractall("dataset_folder")

fp_zarr = Path("dataset_folder") / zarr_root

# find the zarr root inside of dataset_folder by looking for the .zarr extension

# Use xarray's open_zarr function with the in-memory ZipFile
ds = xr.open_zarr(fp_zarr, consolidated=True)

# Display the dataset
print(ds)
