import numpy as np

from constant import LAT_TICKS_INTERVAL, LON_TICKS_INTERVAL


class TicksLocation:
    def __init__(self) -> None:
        self.xloc = np.arange(0, 180 + 0.00000001, LON_TICKS_INTERVAL)
        self.yloc = np.arange(0, 90 + 0.00000001, LAT_TICKS_INTERVAL)
