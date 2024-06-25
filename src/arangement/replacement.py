import xarray as xr
from xarray import Dataset

from util.path_complement import generate_path


class DimensionArrayReplacement:
    def __init__(self, wrfout_path: str) -> None:
        self.data = xr.open_dataset(wrfout_path)
        self.data = self.replace_dim_array()

    def replace_dim_array(self) -> Dataset:
        lat = self.data["XLAT"].sel(west_east=0, Time=0).values
        lon = self.data["XLONG"].sel(south_north=0, Time=0).values
        time = self.data["XTIME"].values
        self.data = self.data.assign_coords(
            south_north=lat, west_east=lon, Time=time
        )
        return self.data
