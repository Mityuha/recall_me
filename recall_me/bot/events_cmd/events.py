from typing import Callable, Final, Iterable
from uuid import uuid4

from telegram import InlineKeyboardMarkup, Message, Update
from telegram.ext import ContextTypes

from .interfaces import Event, EventsGetter, StorageSave
from .types import AllEventsState


class EventsCommand:
    def __init__(
        self,
        *,
        storage: StorageSave,
        events_getter: EventsGetter,
        events_reply_markup: Callable,
    ) -> None:
        self.events_getter: Final[EventsGetter] = events_getter
        self.storage: Final[StorageSave] = storage
        self.events_reply_markup: Final[Callable] = events_reply_markup

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not update.message:
            return
        message: Message = update.message

        if not message.from_user:
            return

        events: Iterable[Event] = await self.events_getter.get_user_events(
            str(message.from_user.id)
        )

        user_id: str = str(message.from_user.id)
        state: AllEventsState = AllEventsState.CMD_ALL_EVENTS_SCREEN
        callback_id: str = str(uuid4())
        reply_markup: InlineKeyboardMarkup = self.events_reply_markup(
            callback_id=callback_id,
            events=events,
        )
        await message.reply_text(
            "Ваши события",
            reply_markup=reply_markup,
        )
        await self.storage.save_state(
            callback_id=callback_id,
            user_id=user_id,
            previous_state=AllEventsState.NO_MESSAGE,
            current_state=state,
            metadata=None,
        )
