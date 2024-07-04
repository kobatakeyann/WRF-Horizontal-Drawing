# # from datetime import datetime

# # from arangement.replacement import DimensionArrayReplacement

wrfout_path = "/work1/kobatake_yusuke/WRF/analysis/drawing/data/wrfout/wrfout_nestingtest_d03_2023-08-21_00:00:00"
# a = DimensionArrayReplacement(wrfout_path)
# first = a.dataset["Time"].values[0]

# # first = datetime(2023, 8, 21, 0, 0)
# # print(first)
# # print(a.dataset["Time"].sel(Time=first))
# # pressure = (
# #     a.dataset["PB"].isel(Time=0, south_north=0, west_east=0).values
# #     + a.dataset["P"].isel(Time=0, south_north=0, west_east=0).values
# # )

# pressure = a.dataset["P_HYD"].isel(Time=0, south_north=0, west_east=0).values

from netCDF4 import Dataset
from wrf import ALL_TIMES, getvar, latlon_coords, to_np

# # "QV"
# # "T2"
# # "QVAPOR"
# # print(pressure / 100)
# print(pressure / 100)
from xarray import open_dataset

# ds = open_dataset(wrfout_path)
ds = Dataset(wrfout_path)
# umet = getvar(ds, "uvmet")
# print(umet.shape)
# lon = getvar(ds, "lon")
# lat = getvar(ds, "lat")

dy = to_np(getvar(ds, "DX2D"))
print(dy)


# t = getvar(ds, "RAINNC")
# print(t)

# print(ds["RAINNC"].description)
# uvmet = getvar(ds, "uvmet")
# print(uvmet.description)
# print("bottom_top" in uvmet.dims)
# times = getvar(ds, "times", timeidx=ALL_TIMES)
# print(uvmet.sel(west_east=130).values.shape)
# print(to_np(lon).shape)
# lat, lon = latlon_coords(uvmet)
# print(to_np(lon).shape)
# from arangement.slicing import Slicing

# a = Slicing(wrfout_path)
# print(a.datetimes)


# class Slicing:
#     def __init__(self, wrfout_path: str) -> None:
#         self.nc_ds = nc.Dataset(wrfout_path)
#         extracted_dt = to_np(self.get_var_dataset("times"))
#         self.formatted_dt = get_formatted_times(extracted_dt)

#     def get_var_dataset(self, varname: str) -> DataArray:
#         var_dataset = getvar(self.nc_ds, varname, timeidx=ALL_TIMES)
#         self.var_ds = var_dataset
#         return var_dataset

#     def get_2d_ds_at_p_plain(self, varname: str, pressure: float) -> None:
#         target_var_ds = self.get_var_dataset(varname)
#         pressure_ds = self.get_var_dataset("p")
#         self.var_ds = interplevel(target_var_ds, pressure_ds, pressure)

#     def get_2d_ds_at_levels(self, varname: str, height: float) -> None:
#         target_var_ds = self.get_var_dataset(varname)
#         height_ds = self.get_var_dataset("z")
#         self.var_ds = interplevel(target_var_ds, height_ds, height)

#     def slice_in_lat_dim(self) -> None:
#         self.var_ds = self.var_ds.sel(south_north=slice(LAT_START, LAT_END))

#     def slice_in_lon_dim(self) -> None:
#         self.var_ds = self.var_ds.sel(west_east=slice(LON_START, LON_END))

#     def slice_in_time_dim(self, datetime: datetime) -> DataArray:
#         self.var_ds = self.var_ds.sel(Time=datetime, method="nearest")

#     def get_var_array(self, varname: str, datetime: datetime) -> ndarray:
#         var_dims = getvar(self.nc_ds, varname).dims
#         if "bottom_top" in var_dims:
#             self.get_2d_ds_at_p_plain(varname, PRESSURE_PLAIN)
#         else:
#             self.get_var_dataset(varname)
#         self.slice_in_time_dim(datetime)
#         self.lat, self.lon = latlon_coords(self.var_ds)
#         return to_np(self.var_ds)

#     def get_precipitation_array(self, time_index: int) -> ndarray:
#         rainnc_ds = self.get_var_dataset("RAINNC")
#         rainc_ds = self.get_var_dataset("RAINC")
#         accumurated_rain = to_np(rainnc_ds.isel(Time=time_index)) + to_np(
#             rainc_ds.isel(Time=time_index)
#         )
#         if time_index == 0:
#             precipitation = accumurated_rain
#         else:
#             previous_accumurated_rain = to_np(
#                 rainnc_ds.isel(Time=time_index - 1)
#             ) + to_np(rainc_ds.isel(Time=time_index - 1))
#             precipitation = accumurated_rain - previous_accumurated_rain
#         self.lat, self.lon = latlon_coords(rainnc_ds)
#         return precipitation
