from datetime import date

from calendar_view.config import style  # type: ignore
from calendar_view.core.event import EventStyle, EventStyles  # type: ignore

TRANSPARENT = EventStyle(event_border=(0, 0, 0, 0), event_fill=(0, 0, 0, 0))

style.hour_height = 128


class Event:
    def __init__(
        self,
        event: str,
        event_date: date,
        *,
        start_time: int = 10,
        duration: int = 2,
        style: EventStyles = EventStyles.GREEN,
    ) -> None:
        self.e = event
        self.d = event_date
        self.t1 = start_time
        self.duration = duration
        self.style = style
