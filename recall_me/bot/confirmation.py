from collections import namedtuple
from typing import Final, Sequence
from uuid import uuid4

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                      Update)
from telegram.ext import ContextTypes

from ..logging import logger
from .interfaces import Event, Event2Text

Event2Save = namedtuple("Event2Save", "events text voice_id")


class EventsConfirmation:
    def __init__(self, event_formatter: Event2Text) -> None:
        self.event_formatter: Final[Event2Text] = event_formatter
        self.yes_2_events: Final[dict[str, Sequence[Event]]] = {}
        self.no_2_events: Final[dict[str, Sequence[Event]]] = {}
        self.yes_no_binging: Final[dict[str, str]] = {}

    def __str__(self) -> str:
        return "[Confirmation]"

    async def send_confirmation(
        self,
        events: Sequence[Event],
        *,
        message: Message,
    ) -> None:
        yes_callback: str = str(uuid4())
        no_callback: str = str(uuid4())
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=yes_callback),
                InlineKeyboardButton("Нет", callback_data=no_callback),
            ],
        ]

        event_2_save = Event2Save(
            events=events,
            text=message.text or "",
            voice_id=message.voice.file_id if message.voice else None,
        )

        self.yes_2_events[yes_callback] = event_2_save
        self.no_2_events[no_callback] = event_2_save
        self.yes_no_binging[yes_callback] = no_callback
        self.yes_no_binging[no_callback] = yes_callback

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

    async def button(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.callback_query:
            logger.info(f"{self}: update received, but no callback_query found")
            return

        query = update.callback_query
        if not query.data:
            logger.info(f"{self}: no callback query data found.")
            await query.delete_message()
            return

        await query.answer()

        answer: str = query.data
        if answer not in self.yes_no_binging:
            await query.edit_message_text(
                text="Похоже, что сообщение старое. Давай по-новой"
            )
            return

        if answer in self.yes_2_events:
            logger.debug(f"{self}: {query.from_user.username} clicked yes")
            await query.edit_message_text(text="Сохранено")
            no_answer = self.yes_no_binging.pop(answer)
            self.yes_no_binging.pop(no_answer)
            self.yes_2_events.pop(answer)
            self.no_2_events.pop(no_answer)
        else:
            logger.debug(f"{self}: {query.from_user.username} clicked no")
            await query.edit_message_text(text="Хорошо. Попробуйте еще раз.")
            yes_answer = self.yes_no_binging.pop(answer)
            self.yes_no_binging.pop(yes_answer)
            self.yes_2_events.pop(yes_answer)
            self.no_2_events.pop(answer)
