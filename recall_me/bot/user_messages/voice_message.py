from datetime import date
from typing import Final, Sequence

from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes

from .interfaces import (DateParser, Event, EventFormatter, Ogg2WavConverter,
                         TextRecognizer)


class VoiceEvents:
    def __init__(
        self,
        *,
        text_recognizer: TextRecognizer,
        ogg_2_wav: Ogg2WavConverter,
        date_parser: DateParser,
        event_formatter: EventFormatter,
        voice_duration_seconds: int = 10,
    ) -> None:
        self.text_recognizer: Final[TextRecognizer] = text_recognizer
        self.ogg_2_wav: Final[Ogg2WavConverter] = ogg_2_wav
        self.date_parser: Final[DateParser] = date_parser
        self.event_formatter: Final[EventFormatter] = event_formatter
        self.voice_duration_seconds: Final[int] = voice_duration_seconds

    def __str__(self) -> str:
        return "[VoiceEvents]"

    async def __call__(
        self,
        *,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> Sequence[Event]:
        if not update.message or not update.message.voice:
            return []

        if update.message.voice.duration >= self.voice_duration_seconds - 1:
            await update.message.reply_text(
                "Голосовое слишком длинное. "
                f"Постарайтесь уложиться в {self.voice_duration_seconds} ceкунд"
            )
            raise ValueError(
                f"User '{update.message.chat.username}' sent long voice message."
            )

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
        return events
