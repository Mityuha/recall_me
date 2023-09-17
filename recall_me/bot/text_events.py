from datetime import date
from typing import Final, Sequence

from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes

from .interfaces import DateParser, Event, EventFormatter


class TextEvents:
    def __init__(
        self,
        *,
        date_parser: DateParser,
        event_formatter: EventFormatter,
    ) -> None:
        self.date_parser: Final[DateParser] = date_parser
        self.event_formatter: Final[EventFormatter] = event_formatter

    def __str__(self) -> str:
        return "[TextEvents]"

    async def __call__(
        self,
        *,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> Sequence[Event]:
        if not update.message or not update.message.text:
            return []

        text = update.message.text
        logger.debug(f"{self}: message received: {text}")

        raw_events: dict[str, list[date]] = self.date_parser.parse(text)
        logger.debug(f"{self}: events parsed: {raw_events}")

        events: Sequence[Event] = self.event_formatter.format_events(raw_events)
        logger.debug(f"{self}: events formatted: {events}")

        return events
