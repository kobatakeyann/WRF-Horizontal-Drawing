from constant import TITLE
from time_relation.conversion import PaddingDatetime


class TextAquisition(PaddingDatetime):
    def get_title_text(self) -> str:
        title = f"{self.year}/{self.month}/{self.day} {self.hour}{self.minute}JST  {TITLE}"
        return title

    def get_filename(self) -> str:
        filename = f"{self.year}{self.month}{self.day}_{self.hour}{self.minute}JST.jpg"
        return filename
