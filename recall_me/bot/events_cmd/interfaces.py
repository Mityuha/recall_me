from typing import Protocol, Sequence

from ..interfaces import EventInfo as Event
from .types import AllEventsState


class EventsGetter(Protocol):
    async def get_user_events(self, user_id: str) -> Sequence[Event]:
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
