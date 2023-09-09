from datetime import date
from typing import Iterable

from recall_me.calendar import Event, SmartCalendar


def smart_calendar(events: Iterable[Event], title: str = "Notes") -> None:
    smart_calendar = SmartCalendar(title=title, hour_height=100)
    image: bytes = smart_calendar.render(events)
    with open("message.png", "wb") as f:
        f.write(image)


if __name__ == "__main__":
    smart_calendar(
        [
            Event("7 февраля Лерка", date(year=2023, month=2, day=7)),
            Event("7 февраля Митяй", date(year=2023, month=2, day=7)),
            Event("10 февраля Хорошев", date(year=2023, month=2, day=10)),
            Event("17 февраля Aнтон Хорошев", date(year=2023, month=2, day=17)),
            Event("Встреча с митяем какого-то числа", date(year=2023, month=2, day=12)),
            # Event(
            #     "",
            #     date(year=2023, month=2, day=2),
            #     start_time=10,
            #     duration=1,
            #     style=TRANSPARENT,
            # ),
        ]
    )
