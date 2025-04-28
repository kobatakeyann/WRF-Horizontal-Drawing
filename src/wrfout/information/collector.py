from wrf.routines import _VALID_KARGS

from wrfout.loader.xarray_dataset import WrfoutXarrayDataset


class WrfoutInformationCollector:
    def __init__(self, wrfout: WrfoutXarrayDataset) -> None:
        self.wrfout = wrfout
        self.wrfout._set_time_lat_lon_coords()

    def collect_summary(self) -> str:
        ds = self.wrfout.dataset
        lines = [
            "################### Overview ###################",
            f"<< dimension infomation >>\n{ds.dims}\n",
            f"\n<< coordinate infomation >>\n{ds.coords}\n",
            f"\n<< variables infomation >>\n{ds.data_vars}\n",
            "Diagnostics available for wrf-python:",
            "    see https://wrf-python.readthedocs.io/en/latest/user_api/generated/wrf.getvar.html#wrf.getvar\n",
        ]
        lines.extend([f"    {var}" for var in _VALID_KARGS.keys()])
        return "\n".join(lines)

    def collect_details(self) -> str:
        ds = self.wrfout.dataset
        lines = [
            "\n\n\n################### Detail ###################",
            "<< dimension infomation >>",
        ]
        for dim in ds.dims:
            lines.append(f"\n{ds[dim]}")
        lines.append("\n\n<< coordinate infomation >>")
        for coord in ds.coords:
            lines.append(f"\n{ds[coord]}")
        lines.append("\n\n<< variables infomation >>")
        for var in ds.data_vars:
            lines.append(f"\n{ds[var]}")
        return "\n".join(lines)
