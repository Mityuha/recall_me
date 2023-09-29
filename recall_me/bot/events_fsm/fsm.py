from typing import Any, Final

from recall_me.logging import logger
from telegram import CallbackQuery

from .interfaces import StateHandler, StorageSave
from .types import AllEventsState, CallbackMetadata


class CallbackRouter:
    def __init__(
        self,
        *,
        storage: StorageSave,
        handlers: dict[Any, StateHandler],
    ) -> None:
        self.storage: Final[StorageSave] = storage
        self.handlers: Final[dict[Any, StateHandler]] = handlers

    def __str__(self) -> str:
        return "[CallbackRouter]"

    async def route_callback(
        self,
        *,
        callback_id: str,
        callback_data: str,
        callback_metadata: CallbackMetadata,
        query: CallbackQuery,
    ) -> None:
        state: AllEventsState = callback_metadata.state
        user_id = callback_metadata.user_id

        handler: StateHandler | None = self.handlers.get(
            (state, callback_data),
            self.handlers.get(state, None),
        )

        assert handler

        new_state = await handler(
            user_id=user_id,
            callback_id=callback_id,
            callback_data=callback_data,
            query=query,
            state=state,
        )

        logger.info(f"{self}: New state for {user_id=}, {callback_id=}: {new_state = }")

        if new_state == AllEventsState.NO_MESSAGE:
            logger.info(f"{self}: No more message for {user_id}. Close state.")
            return

        await self.storage.save_state(
            callback_id=callback_id,
            user_id=user_id,
            message_id=callback_metadata.message_id,
            current_state=new_state,
        )
