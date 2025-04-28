from datetime import datetime

import numpy as np
import pandas as pd
from numpy.typing import NDArray


def datetime64_to_datetime(np_dt: np.datetime64) -> datetime:
    return datetime.fromtimestamp(np_dt.astype(datetime) * 1e-9)


def datetime64s_to_datetimes(
    datetime64s: NDArray[np.datetime64],
) -> NDArray[np.object_]:
    start_dt = datetime64_to_datetime(datetime64s[0])
    last_dt = datetime64_to_datetime(datetime64s[-1])
    interval_min = (
        (datetime64s[1] - datetime64s[0]).astype("timedelta64[m]").astype(int)
    )
    pd_dt_indexes = pd.date_range(
        start=start_dt,
        end=last_dt,
        freq=f"{interval_min}min",
    )
    return pd.to_datetime(pd_dt_indexes).to_pydatetime()
