from typing import Final

from .interfaces import Event


class Event2Text:
    def __init__(self) -> None:
        self.month_2_text: Final[dict[int, str]] = {
            1: "января",
            2: "февраля",
            3: "марта",
            4: "апреля",
            5: "мая",
            6: "июня",
            7: "июля",
            8: "августа",
            9: "сентября",
            10: "октября",
            11: "ноября",
            12: "декабря",
        }
        self.max_month_len: Final[int] = max(
            len(month) for month in self.month_2_text.values()
        )

    def __call__(self, event: Event) -> str:
        datet: str = (
            f" {event.edate.day}" if event.edate.day < 10 else f"{event.edate.day}"
        )
        montht: str = self.month_2_text[event.edate.month]
        whitespaces: str = " " * (self.max_month_len - len(montht))
        # return f"{datet} {montht}{whitespaces}  {event.title}"
        return f"{datet} {whitespaces}{montht}  {event.title}"
