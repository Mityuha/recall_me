from asyncio import create_task, sleep
from typing import Final, Sequence

from recall_me.logging import logger
from telegram import Message, Update
from telegram.ext import ContextTypes

from .interfaces import Event, EventsConfirmation, EventsGetter


class Handler:
    def __init__(
        self,
        events_getter: EventsGetter,
        *,
        events_confirmation: EventsConfirmation,
        description: str = "Handler",
    ) -> None:
        self.event_getter: Final[EventsGetter] = events_getter
        self.events_confirmation: Final[EventsConfirmation] = events_confirmation
        self._description: Final[str] = description

    def __str__(self) -> str:
        return f"[{self._description}]"

    async def process_in_background(
        self,
        *,
        message: Message,
        events: Sequence[Event],
    ) -> None:
        is_confirmed: bool = await self.events_confirmation.send_confirmation(
            events,
            message=message,
        )

        if not is_confirmed:
            logger.info(f"{self}: User {message.chat.username} declined events saving.")
            return

        logger.info(
            f"{self}: User {message.chat.username} "
            "confirmed events saving. Save events."
        )

    async def __call__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        if not update.message:
            return

        events: Sequence[Event] = await self.event_getter(
            update=update,
            context=context,
        )

        create_task(
            self.process_in_background(
                message=update.message,
                events=events,
            )
        )
        await sleep(0)
