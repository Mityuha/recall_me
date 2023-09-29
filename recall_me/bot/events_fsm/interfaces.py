from typing import Any, Protocol

from telegram import CallbackQuery

from .types import AllEventsState


class StorageSave(Protocol):
    async def save_state(
        self,
        *,
        callback_id: str,
        user_id: str,
        message_id: int,
        current_state: AllEventsState,
    ) -> None:
        ...


class StateHandler(Protocol):
    async def __call__(
        self,
        *,
        user_id: str,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        state: AllEventsState,
    ) -> AllEventsState | tuple[AllEventsState, Any]:
        ...
