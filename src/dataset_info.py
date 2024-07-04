from pathlib import Path

from wrf.routines import _VALID_KARGS
from xarray import Dataset, open_dataset

from time_relation.conversion import get_formatted_times


class WrfoutInfoOutput:
    def __init__(self, wrfout_path: str) -> None:
        self.parent_dir = str(Path(wrfout_path).parents[1])
        self.wrfout_name = Path(wrfout_path).stem
        self.dataset = open_dataset(wrfout_path)
        self.dataset = self.make_time_lat_lon_coords()

    def make_time_lat_lon_coords(self) -> Dataset:
        lat = self.dataset["XLAT"].sel(west_east=0, Time=0).values
        lon = self.dataset["XLONG"].sel(south_north=0, Time=0).values
        time = get_formatted_times(self.dataset["XTIME"].values)
        self.dataset = self.dataset.assign_coords(
            south_north=lat, west_east=lon, Time=time
        )
        return self.dataset

    def output_dataset_information(self) -> None:
        output_path = (
            f"{self.parent_dir}/information/{self.wrfout_name}_info.txt"
        )
        with open(output_path, mode="w") as f:
            f.write("################### Overview ###################\n")
            f.write(f"<< dimension infomation >>\n{self.dataset.dims} \n")
            f.write(f"\n<< coordinate infomation >>\n{self.dataset.coords} \n")
            f.write(
                f"\n<< variables infomation >>\n{self.dataset.data_vars} \n"
            )
            f.write("Diagnostics available for wrf-python:\n")
            f.write(
                "    see https://wrf-python.readthedocs.io/en/latest/user_api/generated/wrf.getvar.html#wrf.getvar\n"
            )
            for var in _VALID_KARGS.keys():
                f.write(f"    {var}\n")
            f.write("\n\n################### Detail ###################\n")
            f.write(f"<< dimension infomation >>\n")
            for dim in self.dataset.dims:
                f.write(f"\n{self.dataset[dim]} \n")
            f.write(f"\n\n<< coordinate infomation >>\n")
            for coord in self.dataset.coords:
                f.write(f"\n{self.dataset[coord]} \n")
            f.write(f"\n\n<< variables infomation >>\n")
            for var in self.dataset.data_vars:
                f.write(f"\n{self.dataset[var]} \n")
