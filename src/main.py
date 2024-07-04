from constant import contour_plot, shade_plot, vector_plot
from dataset_info import WrfoutInfoOutput
from figure.plot import PlotWrfoutData
from util.path_complement import generate_path

if __name__ == "__main__":
    wrfout_path = generate_path(
        # "/data/wrfout/netcdf/wrfout_nestingtest_d03_2023-08-21_00:00:00"
        "/data/wrfout/netcdf/wrfout_nonetest_d03_2021-08-05_00:00:00"
        # "/data/wrfout/netcdf/wrfout_nestingtest_d02_2023-08-21_00:00:00"
        # "/data/wrfout/netcdf/wrfout_nonetest_d02_2021-08-05_00:00:00"
    )
    info = WrfoutInfoOutput(wrfout_path)
    info.output_dataset_information()
    palette = PlotWrfoutData(wrfout_path)
    palette.make_continuous_figs(
        shade_plot=shade_plot,
        contour_plot=contour_plot,
        vector_plot=vector_plot,
    )
