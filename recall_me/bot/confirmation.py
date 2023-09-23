from asyncio import Queue
from asyncio import TimeoutError as AioTimeoutError
from asyncio import wait_for
from collections import namedtuple
from enum import Enum
from typing import Final, Sequence
from uuid import uuid4

from telegram import (CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message)

from ..logging import logger
from .interfaces import Event, Event2Text

Event2Save = namedtuple("Event2Save", "events text voice_id")


class Confirmation(Enum):
    NO = "0"
    YES = "1"


class EventsConfirmation:
    def __init__(
        self,
        channels: dict[str, Queue],
        event_formatter: Event2Text,
        timeout: int = 5 * 60,
    ) -> None:
        self.event_formatter: Final[Event2Text] = event_formatter
        self.channels: Final[dict[str, Queue]] = channels
        self.timeout: Final[int] = timeout

    def __str__(self) -> str:
        return "[Confirmation]"

    async def send_confirmation(
        self,
        events: Sequence[Event],
        *,
        message: Message,
    ) -> bool:
        callback_id: str = str(uuid4())
        yes_callback: str = f"{callback_id}-{Confirmation.YES.value}"
        no_callback: str = f"{callback_id}-{Confirmation.NO.value}"

        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=yes_callback),
                InlineKeyboardButton("Нет", callback_data=no_callback),
            ],
        ]

        channel: Queue = Queue()
        self.channels[callback_id] = channel

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

        data: str = ""
        query: CallbackQuery

        try:
            data, query = await wait_for(channel.get(), self.timeout)
        except AioTimeoutError:
            logger.warning(
                f"{self}: User '{message.chat.username}' "
                f"didn't confirm events for {self.timeout} seconds"
            )
        finally:
            self.channels.pop(callback_id)

        if not data:
            return False

        confirmation: Confirmation = Confirmation(data)

        if confirmation == Confirmation.NO:
            await query.edit_message_text(text="Хорошо. Попробуйте еще раз.")
            return False

        await query.edit_message_text(text="Сохранено")
        return True
