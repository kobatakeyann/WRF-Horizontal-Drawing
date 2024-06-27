from datetime import datetime

from numpy import ndarray
from xarray import Dataset

from arangement.replacement import DimensionArrayReplacement
from constant import LAT_LON_RANGE


class Slicing(DimensionArrayReplacement):
    def slice_in_lat_dir(self) -> None:
        self.dataset = self.dataset.isel(
            south_north=slice(LAT_LON_RANGE["lat"])
        )

    def slice_in_lon_dir(self) -> None:
        self.dataset = self.dataset.sel(west_east=slice(LAT_LON_RANGE["lon"]))

    def slice_in_time_dir(self, datetime: datetime) -> Dataset:
        return self.dataset.sel(Time=datetime, method="nearest")

    def extract_array(self, dataset: Dataset, variable_name: str) -> ndarray:
        array = dataset[variable_name].values
        return array
