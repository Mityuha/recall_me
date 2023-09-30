from typing import Final, Iterable
from uuid import uuid4

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                      Update)
from telegram.ext import ContextTypes

from ..types import NO, YES, AllEventsState
from .interfaces import Event, Event2Text, EventsGetter, StorageSave


class Handler:
    """Handle either text or voice message."""

    def __init__(
        self,
        events_getter: EventsGetter,
        *,
        description: str = "Handler",
        storage: StorageSave,
        event_formatter: Event2Text,
    ) -> None:
        self.event_getter: Final[EventsGetter] = events_getter
        self._description: Final[str] = description
        self.storage: Final[StorageSave] = storage
        self.event_formatter: Final[Event2Text] = event_formatter

    def __str__(self) -> str:
        return f"[{self._description}]"

    async def __call__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        if not update.message:
            return

        message: Message = update.message

        events: Iterable[Event] = await self.event_getter(
            update=update,
            context=context,
        )

        callback_id: str = str(uuid4())
        yes_callback: str = f"{callback_id}-{YES}"
        no_callback: str = f"{callback_id}-{NO}"

        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=yes_callback),
                InlineKeyboardButton("Нет", callback_data=no_callback),
            ],
        ]

        events_text: str = "\n".join(self.event_formatter(event) for event in events)

        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(keyboard)

        text: str = "\n".join(
            [
                "Если даты правильные, нажимай 'Да'",
                "<pre>",
                events_text,
                "</pre>",
            ]
        )

        await message.reply_text(
            text,
            reply_markup=reply_markup,
            # parse_mode="MarkdownV2",
            parse_mode="HTML",
        )

        metadata: dict = {
            "voice_file_id": message.voice.file_id if message.voice else None,
            "message_text": message.text,
            "events": [
                {
                    "title": e.title,
                    "description": e.description,
                    "edate": e.edate,
                    "start_hour": e.start_hour,
                    "duration": e.duration,
                }
                for e in events
            ],
        }

        await self.storage.save_state(
            callback_id=callback_id,
            user_id=str(message.chat.id),
            previous_state=AllEventsState.NO_MESSAGE,
            current_state=AllEventsState.SAVE_EVENTS_SCREEN,
            metadata=metadata,
        )
