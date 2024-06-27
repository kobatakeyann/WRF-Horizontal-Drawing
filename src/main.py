from constant import contour_plot, grid_line, shade_plot, vector_plot
from figure.plot import PlotWrfoutData
from util.path_complement import generate_path

if __name__ == "__main__":
    wrfout_path = generate_path(
        "/data/wrfout/wrfout_nestingtest_d03_2023-08-21_00:00:00"
    )
    palette = PlotWrfoutData(wrfout_path)
    # palette.make_continuous_figs(
    # shade_plot=shade_plot, contour_plot=contour_plot, grid_line=grid_line
    # )
    palette.make_continuous_precipation_figs(
        contour_plot=contour_plot, grid_line=grid_line, vector_plot=vector_plot
    )
