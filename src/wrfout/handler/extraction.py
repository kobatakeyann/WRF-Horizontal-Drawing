from datetime import datetime
from typing import Callable, cast

import xarray as xr
from wrf import getvar, interplevel

from wrfout.handler.calculation import DiagnosticsCalculation
from wrfout.handler.type import VectorComponent
from wrfout.loader.nc_dataset import WrfoutNetcdfDataset


class BaseExtractor:
    def __init__(self, loader: WrfoutNetcdfDataset) -> None:
        self.loader = loader
        self.loader.load()

    def get_data_array(
        self, varname: str, datetime: datetime, pressure_hpa: int | None = None
    ) -> xr.DataArray:
        var_dataset = cast(
            xr.DataArray,
            getvar(
                self.loader.dataset,
                varname,
                timeidx=self.loader.datetime_index_map[datetime],
            ),
        )
        # variable at surface plain
        if "bottom_top" not in var_dataset.dims:
            return var_dataset

        # variable at all pressure levels
        if pressure_hpa is None:
            return var_dataset
        # variable at pressure plain
        return self.interpolate_at_p_plain(varname, datetime, pressure_hpa)

    def interpolate_at_p_plain(
        self, varname: str, datetime: datetime, pressure_hpa: int
    ) -> xr.DataArray:
        target_var_ds = self.get_data_array(varname, datetime)
        pressure_ds = self.get_data_array("p", datetime)
        interpolated_var_ds = interplevel(
            target_var_ds, pressure_ds, pressure_hpa * 100
        )
        interpolated_var_ds.attrs["description"] = target_var_ds.description
        return interpolated_var_ds

    def interpolate_at_level(
        self, varname: str, datetime: datetime, height_m: int
    ) -> xr.DataArray:
        target_var_ds = self.get_data_array(varname, datetime)
        height_ds = self.get_data_array("z", datetime)
        return interplevel(target_var_ds, height_ds, height_m)


class VariableExtractor(BaseExtractor):
    def __init__(self, loader: WrfoutNetcdfDataset) -> None:
        super().__init__(loader)
        self._additional_var_getters: dict[
            str,
            Callable[
                [str, datetime, bool, int | None],
                xr.DataArray | VectorComponent,
            ],
        ] = {
            "moisture_flux": self._calc_moisture_flux,
            "precipitation": self._calc_precipitation,
            "divergence": self._calc_divergence,
        }

    def get_var_array(
        self,
        varname: str,
        datetime: datetime,
        is_surface: bool,
        pressure: int | None = None,
    ) -> xr.DataArray | VectorComponent:
        for key, func in self._additional_var_getters.items():
            if key in varname:
                return func(varname, datetime, is_surface, pressure)
        return super().get_data_array(varname, datetime, pressure)

    def _calc_precipitation(
        self,
        _: str,
        datetime: datetime,
        is_surface: bool,
        pressure: int | None,
    ) -> xr.DataArray:
        if not is_surface:
            raise ValueError(
                "Precipitation is only available at surface plain."
            )
        time_index = self.loader.datetime_index_map[datetime]
        rainnc = getvar(self.loader.dataset, "RAINNC", timeidx=time_index)
        rainc = getvar(self.loader.dataset, "RAINC", timeidx=time_index)
        accumurated_rain = cast(xr.DataArray, rainnc + rainc)
        if time_index == 0:
            accumurated_rain.attrs["description"] = "hourly precipitation"
            return cast(xr.DataArray, accumurated_rain)
        previous_accumurated_rain = getvar(
            self.loader.dataset, "RAINNC", timeidx=time_index - 1
        ) + getvar(self.loader.dataset, "RAINC", timeidx=time_index - 1)
        hourly_precipitation = (
            (accumurated_rain - previous_accumurated_rain)
            * 60
            / self.loader.wrfout_interval_min
        )
        hourly_precipitation.attrs["description"] = "hourly precipitation"
        return hourly_precipitation

    def _calc_moisture_flux(
        self,
        varname: str,
        datetime: datetime,
        is_surface: bool,
        pressure: int | None,
    ) -> VectorComponent:
        if is_surface:
            wind_u = super().get_data_array("U10", datetime)
            wind_v = super().get_data_array("V10", datetime)
            mixing_ratio = super().get_data_array("Q2", datetime)
            return VectorComponent(
                mixing_ratio * 1000 * wind_u,
                mixing_ratio * 1000 * wind_v,
            )
        pressure = cast(int, pressure)
        wind_uv = self.interpolate_at_p_plain("uvmet", datetime, pressure)
        wind_u = wind_uv[0, :, :]
        wind_v = wind_uv[1, :, :]
        mixing_ratio = self.interpolate_at_level("QVAPOR", datetime, pressure)
        return VectorComponent(
            mixing_ratio * 1000 * wind_u,
            mixing_ratio * 1000 * wind_v,
        )

    def _calc_divergence(
        self,
        varname: str,
        datetime: datetime,
        is_surface: bool,
        pressure: int | None,
    ) -> xr.DataArray:
        if is_surface:
            wind_u = super().get_data_array("U10", datetime)
            wind_v = super().get_data_array("V10", datetime)
            mixing_ratio = super().get_data_array("Q2", datetime)
        else:
            pressure = cast(int, pressure)
            wind_uv = self.interpolate_at_p_plain("uvmet", datetime, pressure)
            wind_u = wind_uv[0, :, :]
            wind_v = wind_uv[1, :, :]
            mixing_ratio = self.interpolate_at_level(
                "QVAPOR", datetime, pressure
            )
        # calculate divergence of wind
        if "wind" in varname:
            u, v = wind_u, wind_v
        # calculate divergence of moisture flux
        elif "moisture" in varname or "vapor" in varname:
            u = mixing_ratio * 1000 * wind_u
            v = mixing_ratio * 1000 * wind_v
        calculator = DiagnosticsCalculation(self.loader)
        return calculator.calc_divergence(u, v)
