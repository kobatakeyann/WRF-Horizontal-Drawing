import matplotlib.style as mplstyle
from cartopy.mpl.geoaxes import GeoAxes

from constants.configuration import (
    LAT_TICKS_INTERVAL,
    LON_TICKS_INTERVAL,
    is_deg_min_format,
)
from constants.constant import GRIDLINE_COLOR, GRIDLINE_WIDTH, grid_line
from figure.map.map_axes import MapAxesController


def make_blank_map(ax: GeoAxes) -> GeoAxes:
    mplstyle.use("fast")
    map_ax = MapAxesController(ax)
    map_ax.plot_coastline()
    map_ax.plot_pref_border()
    map_ax.set_ticks(
        lon_interval=LON_TICKS_INTERVAL, lat_interval=LAT_TICKS_INTERVAL
    )
    if is_deg_min_format:
        map_ax.express_in_deg_min_format()
    if grid_line:
        map_ax.draw_gridlines(color=GRIDLINE_COLOR, width=GRIDLINE_WIDTH)
    map_ax.narrow_down_the_plot_area()
    return map_ax.ax
