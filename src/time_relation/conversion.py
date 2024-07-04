from datetime import datetime, timedelta

import pandas as pd
from numpy import datetime64, ndarray

from constant import WRFOUT_INTERVAL


class PaddingDatetime:
    def __init__(self, target_dt: datetime) -> None:
        self.year, self.month, self.day, self.hour, self.minute = (
            self.pad_with_zero(target_dt.year, 4),
            self.pad_with_zero(target_dt.month, 2),
            self.pad_with_zero(target_dt.day, 2),
            self.pad_with_zero(target_dt.hour, 2),
            self.pad_with_zero(target_dt.minute, 2),
        )

    def pad_with_zero(self, datatime_factor: int, digit: int) -> str:
        return str(datatime_factor).zfill(digit)


def datetime64_to_datetime(np_dt: datetime64) -> datetime:
    return datetime.fromtimestamp(np_dt.astype(datetime) * 1e-9)


def get_formatted_times(datetimes: ndarray) -> ndarray:
    start_dt = datetime64_to_datetime(datetimes[0])
    end_dt = datetime64_to_datetime(datetimes[-1])
    interval_minutes = WRFOUT_INTERVAL
    times = pd.date_range(
        start=start_dt,
        end=end_dt,
        freq=f"{interval_minutes}min",
    )
    times_np = pd.to_datetime(times).to_pydatetime()
    return times_np


def utc_to_jst(utc_dt: datetime) -> datetime:
    time_difference = timedelta(hours=9)
    jst_dt = utc_dt + time_difference
    return jst_dt
