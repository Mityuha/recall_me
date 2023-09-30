from typing import Any, Final

from recall_me.logging import logger
from telegram import CallbackQuery

from .interfaces import CallbackMetadata, StateHandler, Storage
from .types import AllEventsState


class CallbackRouter:
    def __init__(
        self,
        *,
        storage: Storage,
        handlers: dict[Any, StateHandler],
    ) -> None:
        self.storage: Final[Storage] = storage
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
        state: AllEventsState = callback_metadata.current_state
        user_id = callback_metadata.user_id

        handler: StateHandler | None = self.handlers.get(
            (state, callback_data),
            self.handlers.get(state, None),
        )

        assert handler

        new_state = await handler(
            callback_id=callback_id,
            callback_data=callback_data,
            query=query,
            metadata=callback_metadata,
        )
        metadata: Any | None = None

        if isinstance(new_state, tuple):
            new_state, metadata = new_state

        logger.info(
            f"{self}: New state for {user_id=}, "
            f"{callback_id=}: {new_state = }, {metadata = }"
        )

        if new_state == AllEventsState.NO_MESSAGE:
            logger.info(f"{self}: No more message for {user_id}. Close state.")
            await self.storage.drop_state(callback_id)
            return

        await self.storage.save_state(
            callback_id=callback_id,
            user_id=user_id,
            previous_state=state,
            current_state=new_state,
            metadata=metadata,
        )
