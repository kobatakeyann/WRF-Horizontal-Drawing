import pickle
from typing import cast

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes

from constants.configuration import (
    CONTOUR_ADDITION,
    CONTOUR_MULTIPLIER,
    SHADE_ADDITION,
    SHADE_MULTIPLIER,
)
from constants.constant import (
    VAR_INFO_XLOCATION,
    VAR_INFO_YLOCATION,
    VECTOR_MULTIPLIER,
    cbar_auto_ticks,
)
from figure.maker.fig_axes import FigureAxesController
from figure.map.plot import make_blank_map
from figure.property.fig_property import FigureProperties


class Drawer:
    def __init__(self, props: FigureProperties) -> None:
        self._props = props
        fig = plt.figure(figsize=self._props.figsize)
        ax = cast(
            GeoAxes,
            fig.add_axes(
                (0.11, 0.15, 0.8, 0.8),
                projection=ccrs.PlateCarree(),
            ),
        )
        ax = make_blank_map(ax)
        self.basefig = pickle.dumps(fig, protocol=pickle.HIGHEST_PROTOCOL)

    def plot_shade(
        self,
        ax: FigureAxesController,
        x: xr.DataArray,
        y: xr.DataArray,
        array: xr.DataArray,
        var_description: str,
    ) -> None:
        ax.plot_shading(
            x,
            y,
            array * SHADE_MULTIPLIER + SHADE_ADDITION,
        )
        ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        ax.set_cbar_label()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION,
            f"shade    :  {var_description}",
        )

    def plot_contour(
        self,
        ax: FigureAxesController,
        x: xr.DataArray,
        y: xr.DataArray,
        array: xr.DataArray,
        var_description: str,
    ) -> None:
        ax.plot_contour(
            x,
            y,
            array * CONTOUR_MULTIPLIER + CONTOUR_ADDITION,
        )
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.03,
            f"contour :  {var_description}",
        )

    def plot_vector(
        self,
        ax: FigureAxesController,
        x: xr.DataArray,
        y: xr.DataArray,
        u_component: xr.DataArray,
        v_component: xr.DataArray,
        var_description: str,
    ) -> None:
        ax.plot_vector(
            x,
            y,
            u_component * VECTOR_MULTIPLIER,
            v_component * VECTOR_MULTIPLIER,
        )
        ax.plot_legend_vector()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.06,
            f"vector   :  {var_description}",
        )
