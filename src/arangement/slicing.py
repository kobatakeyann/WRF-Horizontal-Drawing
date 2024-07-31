import warnings
from datetime import datetime

import netCDF4 as nc
import numpy as np
from nakametpy.kinematics import divergence_2d
from numpy import ndarray
from wrf import ALL_TIMES, getvar, interplevel, latlon_coords, to_np
from xarray import DataArray

from constant import PRESSURE_PLAIN
from time_relation.conversion import get_formatted_times


class Slicing:
    def __init__(self, wrfout_path: str) -> None:
        self.nc_ds = nc.Dataset(wrfout_path)
        extracted_dt = to_np(getvar(self.nc_ds, "times", timeidx=ALL_TIMES))
        self.formatted_dt = get_formatted_times(extracted_dt)
        self.time_dict = {
            datetime: index for index, datetime in enumerate(self.formatted_dt)
        }

    def get_var_array(self, varname: str, datetime: datetime) -> ndarray:
        var_dims = getvar(self.nc_ds, varname).dims
        if "bottom_top" in var_dims:
            self.get_2d_ds_at_p_plain(varname, PRESSURE_PLAIN * 100, datetime)
        else:
            self.get_var_dataset(varname, datetime)
        self.lat, self.lon = latlon_coords(self.var_ds)
        return to_np(self.var_ds)

    def get_var_dataset(self, varname: str, datetime: datetime) -> DataArray:
        var_dataset = getvar(
            self.nc_ds, varname, timeidx=self.time_dict[datetime]
        )
        self.var_ds = var_dataset
        return var_dataset

    def get_divergence_array(
        self, varname: str, datetime: datetime
    ) -> ndarray:
        dx = to_np(self.get_var_array("DX2D", datetime))
        dy = to_np(self.get_var_array("DX2D", datetime))
        if "surface" in varname:
            u_wind = to_np(self.get_var_dataset("U10", datetime))
            v_wind = to_np(self.get_var_dataset("V10", datetime))
            mixing_ratio = to_np(self.get_var_dataset("Q2", datetime))
            self.lat, self.lon = latlon_coords(self.var_ds)
        else:
            u_wind = self.get_var_array("uvmet", datetime)[0, :, :]
            v_wind = self.get_var_array("uvmet", datetime)[1, :, :]
            mixing_ratio = self.get_var_array("QVAPOR", datetime)
        if "wind" in varname:
            u = u_wind
            v = v_wind
            self.var_ds.attrs["description"] = "divergence of horizontal wind"
        elif "moisture" in varname or "vapor" in varname:
            u = mixing_ratio * 1000 * u_wind
            v = mixing_ratio * 1000 * v_wind
            self.var_ds.attrs["description"] = "divergence of water vapor flux"
        warnings.simplefilter("ignore", FutureWarning)
        divergence_array = divergence_2d(
            u, v, np.delete(dx, -1, 1), np.delete(dy, -1, 0), wrfon=1
        )
        return divergence_array

    def get_2d_ds_at_p_plain(
        self, varname: str, pressure: float, datetime: datetime
    ) -> None:
        target_var_ds = self.get_var_dataset(varname, datetime)
        pressure_ds = self.get_var_dataset("pressure", datetime)
        self.var_ds = interplevel(target_var_ds, pressure_ds, pressure)
        self.var_ds.attrs["description"] = target_var_ds.description

    def get_2d_ds_at_levels(
        self, varname: str, height: float, datetime: datetime
    ) -> None:
        target_var_ds = self.get_var_dataset(varname, datetime)
        height_ds = self.get_var_dataset("z", datetime)
        self.var_ds = interplevel(target_var_ds, height_ds, height)
        self.var_ds.attrs["description"] = target_var_ds.description

    def get_moisture_flux(self, varname: str, datetime: datetime) -> None:
        if "surface" in varname:
            u_wind = to_np(self.get_var_dataset("U10", datetime))
            v_wind = to_np(self.get_var_dataset("V10", datetime))
            mixing_ratio = to_np(self.get_var_dataset("Q2", datetime))
            self.lat, self.lon = latlon_coords(self.var_ds)
        else:
            u_wind = self.get_var_array("uvmet", datetime)[0, :, :]
            v_wind = self.get_var_array("uvmet", datetime)[1, :, :]
            mixing_ratio = self.get_var_array("QVAPOR", datetime)
        self.moisture_flux_u = mixing_ratio * u_wind
        self.moisture_flux_v = mixing_ratio * v_wind
        self.var_ds.attrs["description"] = "water vapor flux"

    def get_precipitation_array(self, datetime: datetime) -> ndarray:
        time_index = self.time_dict[datetime]
        rainnc_ds = getvar(self.nc_ds, "RAINNC", timeidx=time_index)
        rainc_ds = getvar(self.nc_ds, "RAINC", timeidx=time_index)
        accumurated_rain = to_np(rainnc_ds) + to_np(rainc_ds)
        if time_index == 0:
            precipitation = accumurated_rain
        else:
            previous_accumurated_rain = to_np(
                getvar(self.nc_ds, "RAINNC", timeidx=time_index - 1)
            ) + to_np(getvar(self.nc_ds, "RAINC", timeidx=time_index - 1))
            precipitation = accumurated_rain - previous_accumurated_rain
        self.lat, self.lon = latlon_coords(rainnc_ds)
        self.var_ds = rainnc_ds
        return precipitation


class ArrayExtraction(Slicing):
    def get_array_for_shade(
        self, shade_varname: str, datetime: datetime, wrfout_interval: int
    ) -> ndarray:
        if shade_varname == "RAINNC" or shade_varname == "RAINC":
            shade_array = self.get_precipitation_array(datetime) * (
                60 / wrfout_interval
            )
        elif "divergence" in shade_varname:
            shade_array = self.get_divergence_array(shade_varname, datetime)
        elif "water_vapor_flux" in shade_varname:
            self.get_moisture_flux(shade_varname, datetime)
            u_data = self.moisture_flux_u
            v_data = self.moisture_flux_v
            shade_array = (u_data**2 + v_data**2) ** 0.5
        else:
            shade_array = self.get_var_array(shade_varname, datetime)
        return shade_array

    def get_array_for_contour(
        self, contour_varname: str, datetime: datetime
    ) -> ndarray:
        contour_array = self.get_var_array(contour_varname, datetime)
        return contour_array

    def get_array_for_vector(
        self, u_varname: str, v_varname: str, datetime: datetime
    ) -> "tuple[ndarray, ndarray]":
        if "water_vapor_flux" in u_varname:
            self.get_moisture_flux(u_varname, datetime)
            u_array = self.moisture_flux_u
            v_array = self.moisture_flux_v
        else:
            u_array = self.get_var_array(u_varname, datetime)
            if "u_v" in self.var_ds.dims:
                u_array = u_array[0, :, :]
            v_array = self.get_var_array(v_varname, datetime)
            if "u_v" in self.var_ds.dims:
                v_array = v_array[1, :, :]
        return u_array, v_array
