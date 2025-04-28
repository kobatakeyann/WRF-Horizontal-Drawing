import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from constants.configuration import (
    CBAR_UNIT,
    CONTOUR_COLOR,
    TITLE_SIZE,
    VECTOR_COLOR,
    VECTOR_DENSITY,
    VECTOR_LEDEND_VALUE,
    VECTOR_LEGEND_NAME,
    VECTOR_REDUCTION_SCALE,
    plot_contour_label,
)
from constants.constant import (  # VECTOR_HEADAXIS_LENGTH,; VECTOR_HEADLENGTH,; VECTOR_HEADWIDTH,; VECTOR_WIDTH,
    CBAR_EXTENTION,
    CBAR_LABEL_LOCATION,
    CBAR_LABEL_SIZE,
    CBAR_TICKS_BASE,
    CBAR_TICKS_INTERVAL,
    CONTOUR_LABEL_SIZE,
    CONTOUR_WIDTH,
)
from figure.property.fig_property import FigureProperties


class FigureAxesController:
    def __init__(self, ax: GeoAxes, props: FigureProperties) -> None:
        self.ax = ax
        self._props = props

    def plot_shading(
        self, lon: xr.DataArray, lat: xr.DataArray, data: xr.DataArray
    ) -> None:
        self.shade = self.ax.contourf(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=self._props.cbar_levels,
            cmap=self._props.colormap,
            extend=CBAR_EXTENTION,
        )

    def plot_colorbar(self, is_auto_ticks=True) -> None:
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.2, axes_class=Axes)
        plt.gcf().add_axes(cax)
        if is_auto_ticks:
            self.cbar = plt.colorbar(
                self.shade, cax=cax, orientation="vertical"
            )
        else:
            ticks = mticker.IndexLocator(
                base=CBAR_TICKS_BASE, offset=CBAR_TICKS_INTERVAL
            )
            self.cbar = plt.colorbar(
                self.shade, cax=cax, ticks=ticks, orientation="vertical"
            )

    def set_cbar_label(self) -> None:
        self.cbar.set_label(
            CBAR_UNIT,
            labelpad=CBAR_LABEL_LOCATION,
            y=1.08,
            rotation=0,
            fontsize=CBAR_LABEL_SIZE,
        )

    def plot_contour(
        self, lon: xr.DataArray, lat: xr.DataArray, data: xr.DataArray
    ) -> None:
        self.contour = self.ax.contour(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=self._props.contour_levels,
            linewidths=CONTOUR_WIDTH,
            colors=CONTOUR_COLOR,
        )
        if plot_contour_label:
            self.ax.clabel(
                self.contour,
                levels=self._props.clabel_levels,
                fmt="%.{0[0]}f".format([0]),
                fontsize=CONTOUR_LABEL_SIZE,
            )

    def plot_vector(
        self,
        lon: xr.DataArray,
        lat: xr.DataArray,
        u_component: xr.DataArray,
        v_component: xr.DataArray,
    ) -> None:
        self.vector = self.ax.quiver(
            lon,
            lat,
            u_component,
            v_component,
            transform=ccrs.PlateCarree(),
            regrid_shape=VECTOR_DENSITY,
            scale=VECTOR_REDUCTION_SCALE,
            angles="xy",
            scale_units="xy",
            color=VECTOR_COLOR,
            # width=VECTOR_WIDTH,
            # headwidth=VECTOR_HEADWIDTH,
            # headlength=VECTOR_HEADLENGTH,
            # headaxislength=VECTOR_HEADAXIS_LENGTH,
        )

    def plot_legend_vector(self) -> None:
        self.ax.quiverkey(
            self.vector,
            0.92,
            -0.08,
            VECTOR_LEDEND_VALUE,
            VECTOR_LEGEND_NAME,
            labelpos="E",
            coordinates="axes",
            transform=ccrs.PlateCarree(),
        )

    def set_title(self, title_name: str) -> None:
        self.ax.set_title(title_name, fontsize=TITLE_SIZE)

    def plot_text(self, x_loc: float, y_loc: float, text: str) -> None:
        self.ax.text(
            x_loc,
            y_loc,
            text,
            size=8,
            color="black",
            transform=self.ax.transAxes,
        )

    def save_figure(
        self, fig: Figure, save_dir: str, filename: str, dpi: int
    ) -> None:
        os.makedirs(save_dir, exist_ok=True)
        out_path = os.path.join(save_dir, filename)
        fig.savefig(out_path, dpi=dpi)
