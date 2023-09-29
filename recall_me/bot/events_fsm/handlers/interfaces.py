from datetime import date
from typing import Protocol, Sequence


class EventInfo(Protocol):
    eid: int
    title: str
    description: str
    edate: date
    voice_id: str
    start_hour: int
    duration: int


class EventInfoGetter(Protocol):
    async def get_event_info(self, event_id: str | int) -> EventInfo:
        ...


class EventsGetter(Protocol):
    async def get_user_events(self, user_id: str) -> Sequence[EventInfo]:
        ...
