import xarray as xr
from xarray import Dataset

from time_relation.conversion import get_correct_times


class DimensionArrayReplacement:
    def __init__(self, wrfout_path: str) -> None:
        self.dataset = xr.open_dataset(wrfout_path)
        self.dataset = self.replace_dim_array()

    def replace_dim_array(self) -> Dataset:
        lat = self.dataset["XLAT"].sel(west_east=0, Time=0).values
        lon = self.dataset["XLONG"].sel(south_north=0, Time=0).values
        time = get_correct_times(self.dataset["XTIME"].values)
        self.dataset = self.dataset.assign_coords(
            south_north=lat, west_east=lon, Time=time
        )
        return self.dataset
