import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy import ndarray

from constant import (  # VECTOR_HEADAXIS_LENGTH,; VECTOR_HEADLENGTH,; VECTOR_HEADWIDTH,; VECTOR_WIDTH,
    CBAR_EXTENTION,
    CBAR_LABEL_LOCATION,
    CBAR_LABEL_SIZE,
    CBAR_TICKS_BASE,
    CBAR_TICKS_INTERVAL,
    CBAR_UNIT,
    COLOR_MAP_NAME,
    CONTOUR_COLOR,
    CONTOUR_LABEL_SIZE,
    CONTOUR_WIDTH,
    GRIDLINE_COLOR,
    GRIDLINE_WIDTH,
    TITLE_SIZE,
    VECTOR_COLOR,
    VECTOR_DENSITY,
    VECTOR_LEDEND_VALUE,
    VECTOR_LEGEND_NAME,
    VECTOR_REDUCTION_SCALE,
)
from figure.fig_calculation import get_cbar_levels, get_contour_levels


class BaseAxesMethod:
    def __init__(self, ax: GeoAxes) -> None:
        self.ax = ax

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

    def save_figure(self, fig: Figure, save_dir: str, filename: str) -> None:
        os.makedirs(save_dir, exist_ok=True)
        out_path = f"{save_dir}/{filename}"
        fig.savefig(out_path, dpi=300)


class GeoAxesMethod(BaseAxesMethod):
    def __init__(self, ax: GeoAxes) -> None:
        self.ax = ax

    def plot_shading(self, lon: ndarray, lat: ndarray, data: ndarray) -> None:
        self.shade = self.ax.contourf(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=get_cbar_levels(),
            cmap=COLOR_MAP_NAME,
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

    def plot_contour(self, lon: ndarray, lat: ndarray, data: ndarray) -> None:
        self.contour = self.ax.contour(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=get_contour_levels(),
            linewidths=CONTOUR_WIDTH,
            colors=CONTOUR_COLOR,
        )
        self.ax.clabel(
            self.contour,
            fmt="%.{0[0]}f".format([0]),
            fontsize=CONTOUR_LABEL_SIZE,
        )

    def plot_vector(
        self,
        lon: ndarray,
        lat: ndarray,
        u_component: ndarray,
        v_component: ndarray,
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

    def draw_gridlines(self) -> None:
        gl = self.ax.gridlines(
            draw_labels=True, color=GRIDLINE_COLOR, linewidth=GRIDLINE_WIDTH
        )
        gl.right_labels = False
        gl.top_labels = False
        gl.left_labels = False
        gl.bottom_labels = False
