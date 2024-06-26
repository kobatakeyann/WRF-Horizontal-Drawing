import numpy as np

from constant import (
    LAT_END,
    LAT_START,
    LAT_TICKS_INTERVAL,
    LON_END,
    LON_START,
    LON_TICKS_INTERVAL,
)


class TicksLocation:
    def __init__(self) -> None:
        self.xloc = np.arange(0, 180 + 0.00000001, LON_TICKS_INTERVAL)
        self.yloc = np.arange(0, 90 + 0.00000001, LAT_TICKS_INTERVAL)


def calculate_figsize() -> tuple:
    lat_dif = LAT_END - LAT_START
    lon_dif = LON_END - LON_START
    figsize = (7, int(int(lat_dif) * 7 / int(lon_dif)))
    return figsize
