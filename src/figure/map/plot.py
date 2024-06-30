from cartopy.mpl.geoaxes import GeoAxes

from constant import is_deg_min_format
from figure.map.map_axes import MapAxesMethod


def make_blank_map(ax: GeoAxes) -> GeoAxes:
    map_axis = MapAxesMethod(ax)
    map_axis.plot_coastline()
    map_axis.plot_pref_border()
    map_axis.set_ticks()
    if is_deg_min_format:
        map_axis.express_in_deg_min_format()
    map_axis.narrow_down_the_plot_area()
    return map_axis.ax
