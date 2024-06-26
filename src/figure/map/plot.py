from calculation import calculate_figsize
from cartopy.mpl.geoaxes import GeoAxes
from map_axes import MapAxesMethod

from constant import is_deg_min_format


def make_blank_map(ax: GeoAxes) -> GeoAxes:
    # fig = plt.figure(figsize=calculate_figsize())
    # proj = ccrs.PlateCarree()
    # ax = fig.add_axes((0.1, 0.2, 0.7, 0.7), projection=proj)

    map_axis = MapAxesMethod(ax)
    map_axis.plot_coastline()
    map_axis.plot_pref_border()
    map_axis.set_ticks()
    if is_deg_min_format:
        map_axis.express_in_deg_min_format()
    map_axis.narrow_down_the_plot_area()
    return map_axis.ax
