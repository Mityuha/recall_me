from datetime import date
from typing import Final, Sequence

from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes

from .interfaces import (DateParser, Event, EventFormatter, Ogg2WavConverter,
                         TextRecognizer)


class VoiceHandler:
    def __init__(
        self,
        *,
        text_recognizer: TextRecognizer,
        ogg_2_wav: Ogg2WavConverter,
        date_parser: DateParser,
        event_formatter: EventFormatter,
    ) -> None:
        self.text_recognizer: Final[TextRecognizer] = text_recognizer
        self.ogg_2_wav: Final[Ogg2WavConverter] = ogg_2_wav
        self.date_parser: Final[DateParser] = date_parser
        self.event_formatter: Final[EventFormatter] = event_formatter

    def __str__(self) -> str:
        return "[VoiceHandler]"

    async def __call__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        if not update.message or not update.message.voice:
            return

        # get basic info about the voice note file and prepare it for downloading
        new_file = await context.bot.get_file(update.message.voice.file_id)
        # download the voice note as a file
        ogg_bytes: bytearray = await new_file.download_as_bytearray()

        logger.debug(f"{self}: ogg file received ({len(ogg_bytes)} bytes)")

        wav_bytes: bytes = self.ogg_2_wav.convert(ogg_bytes)

        text: str = self.text_recognizer.recognize(wav_bytes)

        logger.debug(f"{self}: text recognized: {text}")

        raw_events: dict[str, list[date]] = self.date_parser.parse(text)
        logger.debug(f"{self}: events parsed: {raw_events}")

        events: Sequence[Event] = self.event_formatter.format_events(raw_events)
        logger.debug(f"{self}: events formatted: {events}")

        await update.message.reply_text(f"Your events:\n{str(events)}")
