import os

import xarray as xr
from time_relation.conversion import datetime64s_to_datetimes


class WrfoutXarrayDataset:
    def __init__(self, wrfout_path: str) -> None:
        if not os.path.exists(wrfout_path):
            raise FileNotFoundError(f"{wrfout_path} does not exist.")
        self.dataset = xr.open_dataset(wrfout_path)

    def _set_time_lat_lon_coords(self) -> None:
        lat = self.dataset["XLAT"].sel(west_east=0, Time=0).values
        lon = self.dataset["XLONG"].sel(south_north=0, Time=0).values
        time = datetime64s_to_datetimes(self.dataset["XTIME"].values)
        self.dataset = self.dataset.assign_coords(
            south_north=lat, west_east=lon, Time=time
        )
