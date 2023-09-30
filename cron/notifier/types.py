from dataclasses import dataclass
from datetime import date

from calendar_view.core.event import EventStyle  # type: ignore


@dataclass
class Event:
    edate: date
    description: str = ""
    title: str = ""
    start_hour: int = 10
    duration: int = 2
    style: EventStyle = EventStyle.GREEN
