from datetime import datetime, timedelta


def utc_to_jst(utc_dt: datetime) -> datetime:
    TIME_DIFFRENCE = timedelta(hours=9)
    jst_dt = utc_dt + TIME_DIFFRENCE
    return jst_dt
