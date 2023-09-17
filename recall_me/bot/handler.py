from typing import Final, Sequence

from telegram import Update
from telegram.ext import ContextTypes

from .interfaces import Event, EventsGetter


class Handler:
    def __init__(
        self,
        events_getter: EventsGetter,
        *,
        description: str = "Handler",
    ) -> None:
        self.event_getter: Final[EventsGetter] = events_getter
        self._description: Final[str] = description

    def __str__(self) -> str:
        return "[self._description]"

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

        await update.message.reply_text(f"Your events:\n{str(events)}")
