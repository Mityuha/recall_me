from asyncio import Queue
from asyncio import TimeoutError as AioTimeoutError
from asyncio import wait_for
from collections import namedtuple
from enum import Enum
from typing import Final, Sequence
from uuid import uuid4

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                      Update)
from telegram.ext import ContextTypes

from ..logging import logger
from .interfaces import Event, Event2Text

Event2Save = namedtuple("Event2Save", "events text voice_id")


class Confirmation(Enum):
    NO = "0"
    YES = "1"


class EventsConfirmation:
    def __init__(self, event_formatter: Event2Text) -> None:
        self.event_formatter: Final[Event2Text] = event_formatter
        # self.yes_2_events: Final[dict[str, Sequence[Event]]] = {}
        # self.no_2_events: Final[dict[str, Sequence[Event]]] = {}
        # self.yes_no_binging: Final[dict[str, str]] = {}
        self.channels: Final[dict[str, Queue]] = {}
        self.timeout: Final[int] = 5 * 60

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

        try:
            confirmation: Confirmation = await wait_for(channel.get(), self.timeout)
        except AioTimeoutError:
            logger.warning(
                f"{self}: User '{message.chat.username}' "
                f"didn't confirm events for {self.timeout} seconds"
            )
            confirmation = Confirmation.NO
        finally:
            self.channels.pop(callback_id)

        if confirmation == Confirmation.NO:
            return False
        return True

    async def button(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.callback_query:
            logger.info(f"{self}: update received, but no callback_query found")
            return

        query = update.callback_query
        if not query.data:
            logger.info(f"{self}: no callback query data found.")
            await query.delete_message()
            return

        logger.debug(
            f"{self}: Query answer received: '{query.data}' "
            f"from user {query.from_user.username}"
        )
        await query.answer()

        callback_id, answer = query.data.rsplit("-", 1)
        if callback_id not in self.channels:
            await query.edit_message_text(
                text="Похоже, что сообщение старое. Попробуйте еще раз"
            )
            return

        confirmation: Confirmation = Confirmation(answer)
        logger.debug(f"{self}: {query.from_user.username} clicked {confirmation}")
        if confirmation == Confirmation.NO:
            await query.edit_message_text(text="Хорошо. Попробуйте еще раз.")
        else:
            await query.edit_message_text(text="Сохранено")

        await self.channels[callback_id].put(confirmation)
