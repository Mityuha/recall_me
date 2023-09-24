from asyncio import Queue, create_task, sleep
from typing import Final

from telegram import Update
from telegram.ext import ContextTypes

from .interfaces import Event, EventsGetter, EventsScreen


class EventsCommand:
    def __init__(
        self,
        channels: dict[str, Queue],
        *,
        events_getter: EventsGetter,
        events_screen: EventsScreen,
    ) -> None:
        self.channels: Final[dict[str, Queue]] = channels
        self.events_getter: Final[EventsGetter] = events_getter
        self.events_screen: Final[EventsScreen] = events_screen

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not update.message:
            return

        if not update.message.from_user:
            return

        events: list[Event] = await self.events_getter.get_user_events(
            str(update.message.from_user.id)
        )

        create_task(self.events_screen.show_events(update.message, events=events))
        await sleep(0)
