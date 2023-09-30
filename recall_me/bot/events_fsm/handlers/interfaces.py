from datetime import date
from typing import Protocol, Sequence

from ..interfaces import CallbackMetadata  # noqa


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


class EventsDeleter(Protocol):
    async def delete_event(self, event_id: str | int) -> None:
        ...


class EventSaver(Protocol):
    async def save_event(
        self,
        *,
        title: str,
        description: str,
        event_day: int,
        event_month: int,
        voice_id: str | None,
        source_text: str | None,
        author_id: str,
        duration: int = 2,
        start_hour: int = -1,
        notify_before_days: int = 7,
    ) -> None:
        ...
