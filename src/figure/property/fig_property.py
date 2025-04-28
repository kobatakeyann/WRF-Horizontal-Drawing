import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Colormap, ListedColormap

from constants.configuration import (
    COLOR_MAP_NAME,
    CONTOUR_INTERVAL,
    CONTOUR_LABEL_INTERVAL,
    CONTOUR_MAX,
    CONTOUR_MIN,
    LAT_BOTTOM,
    LAT_TOP,
    LON_LEFT,
    LON_RIGHT,
    SHADE_INTERVAL,
    SHADE_MAX,
    SHADE_MIN,
)
from constants.constant import WHITE_PART_NUM_FROM_MIDDLE, paint_all


class FigureProperties:
    def __init__(self) -> None:
        self.figsize = self._calculate_figsize()
        self.cbar_levels = self._get_cbar_levels()
        self.contour_levels = self._get_contour_levels()
        self.clabel_levels = self._get_clabel_levels()
        self.colormap = self._get_color_map()

    def _calculate_figsize(self) -> tuple:
        lat_dif = LAT_TOP - LAT_BOTTOM
        lon_dif = LON_RIGHT - LON_LEFT
        figsize = (8, 8 * float(float(lat_dif) / float(lon_dif)))
        return figsize

    def _get_cbar_levels(self) -> np.ndarray:
        return np.arange(
            float(SHADE_MIN),
            float(SHADE_MAX) + 0.000000000000001,
            float(SHADE_INTERVAL),
        )

    def _get_contour_levels(self) -> np.ndarray:
        return np.arange(
            float(CONTOUR_MIN),
            float(CONTOUR_MAX) + 0.000000000000001,
            float(CONTOUR_INTERVAL),
        )

    def _get_clabel_levels(self) -> np.ndarray:
        return np.arange(
            float(CONTOUR_MIN),
            float(CONTOUR_MAX) + 0.000000000000001,
            float(CONTOUR_LABEL_INTERVAL),
        )

    def _get_color_map(self) -> Colormap | ListedColormap:
        cmap = plt.get_cmap(COLOR_MAP_NAME).copy()
        cmap_array = cmap(np.arange(cmap.N))
        if paint_all:
            return cmap
        number_of_color = int((SHADE_MAX - SHADE_MIN) / SHADE_INTERVAL)
        interval = int(256 / number_of_color)
        c_under, c_over = (
            128 - interval * WHITE_PART_NUM_FROM_MIDDLE,
            128 + interval * WHITE_PART_NUM_FROM_MIDDLE,
        )
        cmap_array[c_under:c_over] = [1, 1, 1, 1]
        return ListedColormap(cmap_array)
