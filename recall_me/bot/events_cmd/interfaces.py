from datetime import date
from typing import Protocol, Sequence

from telegram import Message


class Event(Protocol):
    eid: int
    title: str
    description: str
    edate: date
    voice_id: str
    start_hour: int
    duration: int


EventInfo = Event


class EventsGetter(Protocol):
    async def get_user_events(self, user_id: str) -> Sequence[Event]:
        ...


class EventInfoGetter(Protocol):
    async def get_event_info(self, event_id: str | int) -> EventInfo:
        ...


class EventsScreen(Protocol):
    async def show_events(self, message: Message, events: list[Event]) -> None:
        ...


class EventDeleter(Protocol):
    async def delete_event(self, event_id: str | int) -> None:
        ...
