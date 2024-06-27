import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

from constant import LAT_END, LAT_START, LON_END, LON_START
from figure.map.calculation import TicksLocation
from figure.map.lat_lon_format import format_latitude, format_longitude


class MapAxesMethod:
    def __init__(self, ax: GeoAxes) -> None:
        self.ax = ax

    def plot_coastline(self) -> None:
        self.ax.coastlines(linewidths=1, resolution="10m")

    def plot_pref_border(self) -> None:
        shpfilename = shapereader.natural_earth(
            resolution="10m",
            category="cultural",
            name="admin_1_states_provinces",
        )
        provinces = shapereader.Reader(shpfilename).records()
        prefs = filter(
            lambda province: province.attributes["admin"] == "Japan", provinces
        )
        for pref in prefs:
            geometry = pref.geometry
            self.ax.add_geometries(
                [geometry],
                ccrs.PlateCarree(),
                facecolor="none",
                linestyle="-",
                linewidth=0.15,
            )

    def set_ticks(self) -> None:
        ticks = TicksLocation()
        self.ax.set_xticks(ticks.xloc, crs=ccrs.PlateCarree())
        self.ax.set_yticks(ticks.yloc, crs=ccrs.PlateCarree())
        self.ax.xaxis.set_major_formatter(LongitudeFormatter())
        self.ax.yaxis.set_major_formatter(LatitudeFormatter())

    def express_in_deg_min_format(self) -> None:
        self.ax.xaxis.set_major_formatter(format_longitude)
        self.ax.yaxis.set_major_formatter(format_latitude)

    def narrow_down_the_plot_area(self) -> None:
        self.ax.set_extent(
            (LON_START, LON_END, LAT_START, LAT_END), ccrs.PlateCarree()
        )
