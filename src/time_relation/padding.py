from datetime import datetime


class PaddedDatetime:
    def __init__(self, datetime: datetime) -> None:
        self.year, self.month, self.day, self.hour, self.minute = (
            self._pad_with_zero(datetime.year, 4),
            self._pad_with_zero(datetime.month, 2),
            self._pad_with_zero(datetime.day, 2),
            self._pad_with_zero(datetime.hour, 2),
            self._pad_with_zero(datetime.minute, 2),
        )

    def _pad_with_zero(self, datatime_factor: int, digit: int) -> str:
        return str(datatime_factor).zfill(digit)
