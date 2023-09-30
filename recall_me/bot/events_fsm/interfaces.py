from typing import Any, Protocol

from telegram import CallbackQuery

from .types import AllEventsState


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


class CallbackMetadata(Protocol):
    user_id: str
    previous_state: AllEventsState
    current_state: AllEventsState
    metadata: Any


class StateHandler(Protocol):
    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        metadata: CallbackMetadata,
    ) -> AllEventsState | tuple[AllEventsState, Any]:
        ...
