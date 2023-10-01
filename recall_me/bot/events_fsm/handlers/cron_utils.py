from datetime import date
from types import SimpleNamespace
from typing import TypedDict


class CronEvent(TypedDict):
    eid: int
    title: str
    description: str
    edate: str
    start_hour: int
    duration: int
    voice_id: str | None


def event_dict_to_object(event: CronEvent) -> SimpleNamespace:
    oevent: SimpleNamespace = SimpleNamespace(**event)
    oevent.edate = date.fromisoformat(oevent.edate)
    return oevent
