import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

from constants.configuration import LAT_BOTTOM, LAT_TOP, LON_LEFT, LON_RIGHT
from figure.map.ticks import TicksLocation


class MapAxesController:
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

    def set_ticks(self, lon_interval: float, lat_interval: float) -> None:
        ticks = TicksLocation(lon_interval, lat_interval)
        self.ax.set_xticks(ticks.xloc, crs=ccrs.PlateCarree())
        self.ax.set_yticks(ticks.yloc, crs=ccrs.PlateCarree())
        self.ax.xaxis.set_major_formatter(LongitudeFormatter())
        self.ax.yaxis.set_major_formatter(LatitudeFormatter())

    def express_in_deg_min_format(self) -> None:
        self.ax.xaxis.set_major_formatter(MapAxesController.format_longitude)
        self.ax.yaxis.set_major_formatter(MapAxesController.format_latitude)

    def narrow_down_the_plot_area(self) -> None:
        self.ax.set_extent(
            (LON_LEFT, LON_RIGHT, LAT_BOTTOM, LAT_TOP), ccrs.PlateCarree()
        )

    def draw_gridlines(self, color: str, width: float) -> None:
        gl = self.ax.gridlines(draw_labels=True, color=color, linewidth=width)
        gl.right_labels = False
        gl.top_labels = False
        gl.left_labels = False
        gl.bottom_labels = False

    @staticmethod
    def format_longitude(lon: float, _) -> str:
        degrees = int(lon)
        minutes = abs(int((lon - degrees) * 60))
        if minutes == 0:
            minutes = "00"
        return f"{degrees}°{minutes}'E"

    @staticmethod
    def format_latitude(lat: float, _) -> str:
        degrees = int(lat)
        minutes = abs(int((lat - degrees) * 60))
        if minutes == 0:
            minutes = "00"
        return f"{degrees}°{minutes}'N"
