import pickle
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from wrf import latlon_coords

from constants.configuration import (
    CONTOUR_VARNAME,
    GIF_INTERVAL_TIME,
    GIF_NAME,
    MP4_FPS,
    MP4_NAME,
    PRESSURE_PLAIN,
    SHADE_VARNAME,
    TITLE,
    U_VEXTOR_VARNAME,
    V_VEXTOR_VARNAME,
    contour_plot,
    is_surface,
    shade_plot,
    vector_plot,
)
from constants.constant import IMAGE_DPI
from figure.maker.fig_axes import FigureAxesController
from figure.maker.maker import Drawer
from figure.property.fig_property import FigureProperties
from gif.gif import imgs_to_gif
from mp4.video import imgs_to_mp4
from time_relation.padding import PaddedDatetime
from util.path import generate_path
from wrfout.handler.extraction import VariableExtractor
from wrfout.handler.type import VectorComponent
from wrfout.information.outputter import WrfoutInformationOutputter
from wrfout.loader.nc_dataset import WrfoutNetcdfDataset


def main():
    # Specify the path to the Wrfout file
    wrfout_path = generate_path("/data/wrfout/high_20220728_d02")

    ### output the information of the Wrfout file
    writer = WrfoutInformationOutputter(wrfout_path)
    writer.output_to_file()

    ### Vizualize
    # create instances for visualization
    props = FigureProperties()
    drawer = Drawer(props)
    # create instances for variable extraction
    loader = WrfoutNetcdfDataset(wrfout_path)
    extractor = VariableExtractor(loader=loader)

    # set plain
    pressure = None if is_surface else PRESSURE_PLAIN
    # plot at each datetime
    for datetime in loader.datetime_index_map.keys():
        print(f"Now making {datetime} figure …")
        # get base figure
        basefig = pickle.loads(drawer.basefig)
        base_ax = basefig.get_axes()[0]
        target_ax = FigureAxesController(ax=base_ax, props=props)

        # variable plot
        if shade_plot:
            shade_array = extractor.get_var_array(
                varname=SHADE_VARNAME,
                datetime=datetime,
                is_surface=is_surface,
                pressure=pressure,
            )
            if isinstance(shade_array, VectorComponent):
                shade_array = cast(
                    xr.DataArray, np.sqrt(shade_array.u**2 + shade_array.v**2)
                )
                description = "water vapor flux"
            else:
                description = shade_array.description
            lat, lon = latlon_coords(shade_array)
            drawer.plot_shade(
                target_ax,
                x=lon,
                y=lat,
                array=shade_array,
                var_description=description,
            )
        if contour_plot:
            contour_array = extractor.get_var_array(
                varname=CONTOUR_VARNAME,
                datetime=datetime,
                is_surface=is_surface,
                pressure=pressure,
            )
            lat, lon = latlon_coords(contour_array)
            if isinstance(contour_array, VectorComponent):
                contour_array = cast(
                    xr.DataArray,
                    np.sqrt(contour_array.u**2 + contour_array.v**2),
                )
                description = "water vapor flux"
            else:
                description = contour_array.description
            drawer.plot_contour(
                target_ax,
                x=lon,
                y=lat,
                array=contour_array,
                var_description=description,
            )
        if vector_plot:
            if is_surface:
                content = extractor.get_var_array(
                    varname=U_VEXTOR_VARNAME,
                    datetime=datetime,
                    is_surface=is_surface,
                    pressure=pressure,
                )
                # case of water vapor flux
                if isinstance(content, VectorComponent):
                    u_array = content.u
                    v_array = content.v
                    description = "water vapor flux"
                # case of surface wind vector
                elif "u_v" in content.dims:
                    u_array = content[0, :, :]
                    v_array = content[1, :, :]
                    description = "surface wind"
                else:
                    u_array = content
                    v_array = cast(
                        xr.DataArray,
                        extractor.get_var_array(
                            varname=V_VEXTOR_VARNAME,
                            datetime=datetime,
                            is_surface=is_surface,
                            pressure=pressure,
                        ),
                    )
                    description = u_array.description
            else:
                content = extractor.get_var_array(
                    varname=U_VEXTOR_VARNAME,
                    datetime=datetime,
                    is_surface=is_surface,
                    pressure=pressure,
                )
                # case of water vapor flux
                if isinstance(content, VectorComponent):
                    u_array = content.u
                    v_array = content.v
                    description = "water vapor flux"
                # case of wind at pressure plain
                else:
                    u_array = content[0, :, :]
                    v_array = content[1, :, :]
                    description = u_array.description
            lat, lon = latlon_coords(u_array)
            drawer.plot_vector(
                target_ax,
                x=lon,
                y=lat,
                u_component=u_array,
                v_component=v_array,
                var_description=description,
            )

        # title
        padded_dt = PaddedDatetime(datetime)
        filename = f"{padded_dt.year}{padded_dt.month}{padded_dt.day}_{padded_dt.hour}{padded_dt.minute}JST.jpg"
        saving_rootdir = generate_path(f"/img/{Path(wrfout_path).stem}")
        if is_surface:
            saving_dir = f"{saving_rootdir}/horizontal/surface/"
            title = f"{padded_dt.year}/{padded_dt.month}/{padded_dt.day} {padded_dt.hour}{padded_dt.minute}JST surface {TITLE}"
        else:
            saving_dir = f"{saving_rootdir}/horizontal/{PRESSURE_PLAIN}hPa/"
            title = f"{padded_dt.year}/{padded_dt.month}/{padded_dt.day} {padded_dt.hour}{padded_dt.minute}JST {PRESSURE_PLAIN}hPa {TITLE}"
        target_ax.set_title(title)
        # directory arrangement
        if shade_plot:
            saving_dir += f"_{SHADE_VARNAME}"
        if contour_plot:
            saving_dir += f"_{CONTOUR_VARNAME}"
        if vector_plot:
            saving_dir += f"_{U_VEXTOR_VARNAME}"
        # save
        target_ax.save_figure(
            fig=basefig, save_dir=saving_dir, filename=filename, dpi=IMAGE_DPI
        )
        plt.cla()
        plt.close()

    # make gif
    print("Now making gif …")
    imgs_to_gif(
        imgs_dir_path=saving_dir,
        saved_gif_path=f"{saving_dir}/{GIF_NAME}.gif",
        gif_interval_time=GIF_INTERVAL_TIME,
    )
    # make mp4
    print("Now making mp4 …")
    imgs_to_mp4(
        imgs_dir_path=saving_dir,
        saved_mp4_path=f"{saving_dir}/{MP4_NAME}.mp4",
        fps=MP4_FPS,
    )
    print("Successfully Completed!")


if __name__ == "__main__":
    main()
