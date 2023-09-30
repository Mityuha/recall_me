from datetime import date
from typing import Iterable, Protocol

from recall_me.bot.types import AllEventsState

from .types import Event


class BotUsers(Protocol):
    async def get_bot_users(
        self,
    ) -> Iterable[str]:
        ...


class EventInfo(Protocol):
    eid: int
    title: str
    description: str
    edate: date
    voice_id: str
    start_hour: int
    duration: int


class UserEvents(Protocol):
    async def get_user_events(
        self,
        user_id: str,
        *,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> Iterable[EventInfo]:
        ...


class SmartCalendar(Protocol):
    def render(self, events: Iterable[Event]) -> bytes:
        ...


class StorageSave(Protocol):
    async def save_state(
        self,
        *,
        callback_id: str,
        user_id: str,
        previous_state: AllEventsState,
        current_state: AllEventsState,
        metadata: dict | list | None,
    ) -> None:
        ...
