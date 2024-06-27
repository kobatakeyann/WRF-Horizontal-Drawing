from datetime import datetime

import pandas as pd


def round_min_to_every_10min(datetime: datetime) -> datetime:
    dt_index = pd.date_range(start=datetime, end=datetime, periods=1)
    dt_rounded = dt_index.round("10min")
    return dt_rounded.to_pydatetime()[0]


def round_off_below_sec(datetime: datetime) -> datetime:
    return datetime.replace(second=0, microsecond=0)
