from datetime import date
from typing import Protocol

from calendar_view.core.event import EventStyle  # type: ignore


class SmartTitleI(Protocol):
    def __call__(self, title: str) -> str:
        ...


class Event(Protocol):
    edate: date
    description: str
    title: str
    start_hour: int
    duration: int
    style: EventStyle
