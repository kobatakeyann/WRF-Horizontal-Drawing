import numpy as np
from numpy import ndarray

from constant import (
    CONTOUR_INTERVAL,
    CONTOUR_LABEL_INTERVAL,
    CONTOUR_MAX,
    CONTOUR_MIN,
    LAT_END,
    LAT_START,
    LON_END,
    LON_START,
    SHADE_INTERVAL,
    SHADE_MAX,
    SHADE_MIN,
)


def calculate_figsize() -> tuple:
    lat_dif = LAT_END - LAT_START
    lon_dif = LON_END - LON_START
    figsize = (7, 7 * float(float(lat_dif) / float(lon_dif)))
    return figsize


def get_cbar_levels() -> ndarray:
    levels = np.arange(
        float(SHADE_MIN),
        float(SHADE_MAX) + 0.000000000000001,
        float(SHADE_INTERVAL),
    )
    return levels


def get_contour_levels() -> ndarray:
    levels = np.arange(
        float(CONTOUR_MIN),
        float(CONTOUR_MAX) + 0.000000000000001,
        float(CONTOUR_INTERVAL),
    )
    return levels


def get_clabel_levels() -> ndarray:
    levels = np.arange(
        float(CONTOUR_MIN),
        float(CONTOUR_MAX) + 0.000000000000001,
        float(CONTOUR_LABEL_INTERVAL),
    )
    return levels
