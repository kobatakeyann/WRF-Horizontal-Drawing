import pickle
from datetime import datetime
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from numpy import ndarray

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
from time_relation.conversion import get_correct_times
from util.path_complement import generate_path


class PlotWrfoutData:
    def __init__(self, wrfout_path: str) -> None:
        self.wrfout = Slicing(wrfout_path)
        self.datetimes = get_correct_times(self.wrfout.dataset["XTIME"].values)
        self.save_dir = generate_path(f"/img/{Path(wrfout_path).stem}/")
        fig = plt.figure(figsize=calculate_figsize())
        ax = fig.add_axes(
            (0.11, 0.15, 0.8, 0.8),
            projection=ccrs.PlateCarree(),
        )
        ax = make_blank_map(ax)
        self.basefig = pickle.dumps(fig)

    def make_figure(
        self,
        datetime: datetime,
        shade_plot=False,
        contour_plot=False,
        vector_plot=False,
    ) -> None:

        basefig = pickle.loads(self.basefig)
        target_ax = GeoAxesMethod(plt.gca())
        dataset = self.wrfout.slice_in_time_dir(datetime)
        lon = self.wrfout.extract_array(dataset, "XLONG")
        lat = self.wrfout.extract_array(dataset, "XLAT")
        save_dir = f"{self.save_dir}/horizontal/"
        if shade_plot:
            shade_data = (
                self.wrfout.extract_array(dataset, SHADE_VARNAME)[0, :, :]
                * 1000
            )
            target_ax.plot_shading(lon, lat, shade_data)
            target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
            target_ax.set_cbar_label()
            target_ax.plot_text(
                VAR_INFO_XLOCATION,
                VAR_INFO_YLOCATION,
                f"shade    :  {dataset[SHADE_VARNAME].description}",
            )
            save_dir += f"_{SHADE_VARNAME}_"
        if contour_plot:
            contour_data = self.wrfout.extract_array(dataset, CONTOUR_VARNAME)
            target_ax.plot_contour(lon, lat, contour_data)
            target_ax.plot_text(
                VAR_INFO_XLOCATION,
                VAR_INFO_YLOCATION - 0.04,
                f"contour :  {dataset[CONTOUR_VARNAME].description}",
            )
            save_dir += f"_{CONTOUR_VARNAME}_"
        if vector_plot:
            u_data = self.wrfout.extract_array(dataset, U_VEXTOR_VARNAME)
            v_data = self.wrfout.extract_array(dataset, V_VEXTOR_VARNAME)
            target_ax.plot_vector(lon, lat, u_data, v_data)
            target_ax.plot_legend_vector()
            target_ax.plot_text(
                VAR_INFO_XLOCATION,
                VAR_INFO_YLOCATION - 0.08,
                f"vector   :  {dataset[U_VEXTOR_VARNAME].description}",
            )
            save_dir += f"_{U_VEXTOR_VARNAME}_"
        if grid_line:
            target_ax.draw_gridlines()
        text = TextAquisition(datetime)
        target_ax.set_title(text.get_title_text())
        filename = text.get_filename()
        target_ax.save_figure(
            fig=basefig, save_dir=save_dir, filename=filename
        )
        plt.cla()
        plt.close()

    def make_preciptation_figure(
        self,
        datetime: datetime,
        index: int,
        contour_plot=False,
        vector_plot=False,
    ) -> None:

        basefig = pickle.loads(self.basefig)
        target_ax = GeoAxesMethod(plt.gca())
        dataset = self.wrfout.slice_in_time_dir(datetime)
        lon = self.wrfout.extract_array(dataset, "XLONG")
        lat = self.wrfout.extract_array(dataset, "XLAT")
        save_dir = f"{self.save_dir}/horizontal/"
        shade_data = self.get_precipitation_array(index) * (
            60 / WRFOUT_INTERVAL
        )
        target_ax.plot_shading(lon, lat, shade_data)
        target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        target_ax.set_cbar_label()
        target_ax.plot_text(
            VAR_INFO_XLOCATION,
            VAR_INFO_YLOCATION,
            f"shade    :  precipitation",
        )
        save_dir += f"_{SHADE_VARNAME}_"
        if contour_plot:
            contour_data = self.wrfout.extract_array(dataset, CONTOUR_VARNAME)
            target_ax.plot_contour(lon, lat, contour_data)
            target_ax.plot_text(
                VAR_INFO_XLOCATION,
                VAR_INFO_YLOCATION - 0.04,
                f"contour :  {dataset[CONTOUR_VARNAME].description}",
            )
            save_dir += f"_{CONTOUR_VARNAME}_"
        if vector_plot:
            u_data = self.wrfout.extract_array(dataset, U_VEXTOR_VARNAME)
            v_data = self.wrfout.extract_array(dataset, V_VEXTOR_VARNAME)
            target_ax.plot_vector(lon, lat, u_data, v_data)
            target_ax.plot_legend_vector()
            target_ax.plot_text(
                VAR_INFO_XLOCATION,
                VAR_INFO_YLOCATION - 0.08,
                f"vector   :  {dataset[U_VEXTOR_VARNAME].description}",
            )
            save_dir += f"_{U_VEXTOR_VARNAME}_"
        if grid_line:
            target_ax.draw_gridlines()
        text = TextAquisition(datetime)
        target_ax.set_title(text.get_title_text() + " precipitation")
        filename = text.get_filename()
        target_ax.save_figure(
            fig=basefig, save_dir=save_dir, filename=filename
        )
        plt.cla()
        plt.close()

    def make_continuous_figs(
        self,
        shade_plot=False,
        contour_plot=False,
        vector_plot=False,
    ) -> None:
        for datetime in self.datetimes:
            print(f"Now making {datetime} figure …")
            self.make_figure(
                datetime,
                shade_plot=shade_plot,
                contour_plot=contour_plot,
                vector_plot=vector_plot,
            )
        print("Successfully Completed!")

    def make_continuous_precipation_figs(
        self,
        contour_plot=False,
        vector_plot=False,
    ) -> None:
        for index, datetime in enumerate(self.datetimes):
            print(f"Now making {datetime} figure …")
            self.make_preciptation_figure(
                datetime,
                index,
                contour_plot=contour_plot,
                vector_plot=vector_plot,
            )
        print("Successfully Completed!")

    def get_precipitation_array(self, index: int) -> ndarray:
        time_index = index
        accumurated_rain = (
            self.wrfout.dataset["RAINC"].isel(Time=time_index).values
            + self.wrfout.dataset["RAINNC"].isel(Time=time_index).values
        )
        if time_index == 0:
            precipitation = accumurated_rain
        else:
            previous_accumurated_rain = (
                self.wrfout.dataset["RAINC"].isel(Time=time_index - 1).values
                + self.wrfout.dataset["RAINNC"]
                .isel(Time=time_index - 1)
                .values
            )
            precipitation = accumurated_rain - previous_accumurated_rain
        return precipitation
