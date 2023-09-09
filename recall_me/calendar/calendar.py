from datetime import date
from io import BytesIO
from typing import Final, Iterable

from calendar_view.calendar import Calendar  # type: ignore
from calendar_view.config import style  # type: ignore
from calendar_view.core import data  # type: ignore
from calendar_view.core.event import Event as CEvent  # type: ignore

from .interfaces import SmartTitleI
from .smart_title import SmartTitle
from .types import Event


class SmartCalendar:
    def __init__(
        self,
        *,
        title: str = "Notes",
        smart_title: SmartTitleI = SmartTitle(),
        locale: str = "ru",
        hour_height: int = 128,
    ) -> None:
        self.title: Final[str] = title
        self.smart_title: Final[SmartTitleI] = smart_title
        self.locale: Final[str] = locale
        self.hour_height: Final[int] = hour_height

    def render(self, events: Iterable[Event]) -> bytes:
        min_date: date = date.today()
        max_date: date = date(year=1980, month=1, day=1)
        min_t: int = 24
        max_t: int = 0

        calendar_events: list[CEvent] = []
        for ev in events:
            min_date = min(min_date, ev.d)
            max_date = max(max_date, ev.d)
            min_t = min(min_t, ev.t1)
            max_t = max(max_t, ev.t1 + ev.duration)
            calendar_events.append(
                CEvent(
                    day=ev.d.isoformat(),
                    start=f"{ev.t1}:00",
                    end=f"{ev.t1 + ev.duration}:00",
                    title=self.smart_title(ev.e),
                    notes=ev.e,
                    style=ev.style,
                )
            )

        config = data.CalendarConfig(
            lang=self.locale,
            title=self.title,
            dates=f"{min_date.isoformat()} - {max_date.isoformat()}",
            hours=f"{min_t} - {max_t}",
            show_year=False,
            mode=None,
            title_vertical_align="top",
            legend=False,
        )

        old_hour_height = style.hour_height
        style.hour_height = self.hour_height

        calendar = Calendar.build(config)
        calendar.add_events(calendar_events)
        image: BytesIO = BytesIO()
        calendar.save(image)

        style.hour_height = old_hour_height
        return image.getbuffer()
