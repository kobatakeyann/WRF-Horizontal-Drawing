import warnings

import numpy as np
import xarray as xr
from nakametpy.kinematics import divergence_2d
from wrf import getvar, to_np

from wrfout.loader.nc_dataset import WrfoutNetcdfDataset


class DiagnosticsCalculation:
    def __init__(self, loader: WrfoutNetcdfDataset) -> None:
        self.loader = loader

    def calc_divergence(
        self, u: xr.DataArray, v: xr.DataArray
    ) -> xr.DataArray:
        dx = to_np(getvar(self.loader.dataset, "DX2D"))
        dy = to_np(getvar(self.loader.dataset, "DX2D"))
        warnings.simplefilter("ignore", FutureWarning)
        divergence = divergence_2d(
            u, v, np.delete(dx, -1, -1), np.delete(dy, -1, 0), wrfon=1
        )
        # retain the coordinates
        divergence = xr.DataArray(
            divergence,
            coords={
                "XLONG": u.coords["XLONG"],
                "XLAT": v.coords["XLAT"],
            },
            dims=("south_north", "west_east"),
        )
        divergence.attrs["description"] = "divergence"
        return divergence
