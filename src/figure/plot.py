import pickle
from datetime import datetime
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from arangement.slicing import Slicing
from constant import (
    CONTOUR_VARNAME,
    SHADE_VARNAME,
    U_VEXTOR_VARNAME,
    V_VEXTOR_VARNAME,
    VAR_INFO_XLOCATION,
    VAR_INFO_YLOCATION,
    WRFOUT_INTERVAL,
    cbar_auto_ticks,
    grid_line,
)
from figure.axes_method import GeoAxesMethod
from figure.fig_calculation import calculate_figsize
from figure.fig_text import TextAquisition
from figure.map.plot import make_blank_map
from gif.gif import make_gif_from_imgs
from util.path_complement import generate_path


class PlotWrfoutData:
    def __init__(self, wrfout_path: str) -> None:
        self.wrfout = Slicing(wrfout_path)
        self.save_rootdir = generate_path(f"/img/{Path(wrfout_path).stem}/")
        fig = plt.figure(figsize=calculate_figsize())
        ax = fig.add_axes(
            (0.11, 0.15, 0.8, 0.8),
            projection=ccrs.PlateCarree(),
        )
        ax = make_blank_map(ax)
        self.basefig = pickle.dumps(fig)

    def plot_shade(self, ax: GeoAxesMethod, datetime: datetime) -> None:
        shade_data = self.wrfout.get_var_array(SHADE_VARNAME, datetime)
        ax.plot_shading(self.wrfout.lon, self.wrfout.lat, shade_data)
        ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        ax.set_cbar_label()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION,
            f"shade    :  {self.wrfout.var_ds.description}",
        )
        self.save_dir += f"_{SHADE_VARNAME}_"

    def plot_contour(self, ax: GeoAxesMethod, datetime: datetime) -> None:
        contour_data = self.wrfout.get_var_array(CONTOUR_VARNAME, datetime)
        ax.plot_contour(self.wrfout.lon, self.wrfout.lat, contour_data)
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.04,
            f"contour :  {self.wrfout.var_ds.description}",
        )
        self.save_dir += f"_{CONTOUR_VARNAME}_"

    def plot_vector(self, ax: GeoAxesMethod, datetime: datetime) -> None:
        u_data = self.wrfout.get_var_array(U_VEXTOR_VARNAME, datetime)
        if "u_v" in self.wrfout.var_ds.dims:
            u_data = u_data[0, :, :]
        v_data = self.wrfout.get_var_array(V_VEXTOR_VARNAME, datetime)
        if "u_v" in self.wrfout.var_ds.dims:
            v_data = v_data[1, :, :]
        ax.plot_vector(self.wrfout.lon, self.wrfout.lat, u_data, v_data)
        ax.plot_legend_vector()
        ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION - 0.08,
            f"vector   :  {self.wrfout.var_ds.description}",
        )
        self.save_dir += f"_{U_VEXTOR_VARNAME}_"

    def make_figure(
        self,
        datetime: datetime,
        shade_plot=False,
        contour_plot=False,
        vector_plot=False,
    ) -> None:

        basefig = pickle.loads(self.basefig)
        target_ax = GeoAxesMethod(plt.gca())
        self.save_dir = f"{self.save_rootdir}/horizontal/"
        if shade_plot:
            self.plot_shade(target_ax, datetime)
        if contour_plot:
            self.plot_contour(target_ax, datetime)
        if vector_plot:
            self.plot_vector(target_ax, datetime)
        if grid_line:
            target_ax.draw_gridlines()
        text = TextAquisition(datetime)
        target_ax.set_title(text.get_title_text())
        filename = text.get_filename()
        target_ax.save_figure(
            fig=basefig, save_dir=self.save_dir, filename=filename
        )
        plt.cla()
        plt.close()

    def make_preciptation_figure(
        self,
        datetime: datetime,
        time_index: int,
        contour_plot=False,
        vector_plot=False,
    ) -> None:

        basefig = pickle.loads(self.basefig)
        target_ax = GeoAxesMethod(plt.gca())
        self.save_dir = f"{self.save_rootdir}/horizontal/"
        shade_data = self.wrfout.get_precipitation_array(time_index) * (
            60 / WRFOUT_INTERVAL
        )
        target_ax.plot_shading(self.wrfout.lon, self.wrfout.lat, shade_data)
        target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        target_ax.set_cbar_label()
        target_ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION,
            f"shade    :  precipitation",
        )
        self.save_dir += f"_{SHADE_VARNAME}_"
        if contour_plot:
            self.plot_contour(target_ax, datetime)
        if vector_plot:
            self.plot_vector(target_ax, datetime)
        if grid_line:
            target_ax.draw_gridlines()
        text = TextAquisition(datetime)
        target_ax.set_title(text.get_title_text() + " precipitation")
        filename = text.get_filename()
        target_ax.save_figure(
            fig=basefig, save_dir=self.save_dir, filename=filename
        )
        plt.cla()
        plt.close()

    def make_continuous_figs(
        self,
        shade_plot=False,
        contour_plot=False,
        vector_plot=False,
    ) -> None:
        for datetime in self.wrfout.formatted_dt:
            print(f"Now making {datetime} figure …")
            self.make_figure(
                datetime,
                shade_plot=shade_plot,
                contour_plot=contour_plot,
                vector_plot=vector_plot,
            )
        make_gif_from_imgs(
            self.save_dir, f"{self.save_dir}/temp_variation.gif"
        )
        print("Successfully Completed!")

    def make_continuous_precipation_figs(
        self,
        contour_plot=False,
        vector_plot=False,
    ) -> None:
        for time_index, datetime in enumerate(self.wrfout.formatted_dt):
            print(f"Now making {datetime} figure …")
            self.make_preciptation_figure(
                datetime,
                time_index,
                contour_plot=contour_plot,
                vector_plot=vector_plot,
            )
        make_gif_from_imgs(
            self.save_dir, f"{self.save_dir}/temp_variation.gif"
        )
        print("Successfully Completed!")
