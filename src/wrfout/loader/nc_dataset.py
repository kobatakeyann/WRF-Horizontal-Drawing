import os
from datetime import datetime
from typing import cast

import netCDF4 as nc
import numpy as np
from numpy.typing import NDArray
from time_relation.conversion import datetime64s_to_datetimes
from wrf import ALL_TIMES, getvar, to_np


class WrfoutNetcdfDataset:
    def __init__(self, wrfout_path: str) -> None:
        if not os.path.exists(wrfout_path):
            raise FileNotFoundError(
                f"File not found: {wrfout_path}. Specify a valid path."
            )
        self._wrfout_path = wrfout_path
        self._dataset: nc.Dataset | None = None
        self._wrfout_interval_min: int | None = None
        self._datetime_index_map: dict[datetime, int] = {}

    def load(self) -> None:
        self._dataset = nc.Dataset(self._wrfout_path)
        datetime64s = cast(
            NDArray[np.datetime64],
            to_np(getvar(self._dataset, "times", timeidx=ALL_TIMES)),
        )
        self._wrfout_interval_min = (
            (datetime64s[1] - datetime64s[0])
            .astype("timedelta64[m]")
            .astype(int)
        )
        datetimes = datetime64s_to_datetimes(datetime64s)
        self._datetime_index_map = {
            datetime: index for index, datetime in enumerate(datetimes)
        }

    @property
    def dataset(self) -> nc.Dataset:
        if self._dataset is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        return self._dataset

    @property
    def wrfout_interval_min(self) -> int:
        if self._wrfout_interval_min is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        return self._wrfout_interval_min

    @property
    def datetime_index_map(self) -> dict[datetime, int]:
        if self._datetime_index_map is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        return self._datetime_index_map
