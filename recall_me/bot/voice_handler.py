from typing import Final

from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes

from .interfaces import Ogg2WavConverter, TextRecognizer


class VoiceHandler:
    def __init__(
        self,
        *,
        text_recognizer: TextRecognizer,
        ogg_2_wav: Ogg2WavConverter,
    ) -> None:
        self.text_recognizer: Final[TextRecognizer] = text_recognizer
        self.ogg_2_wav: Final[Ogg2WavConverter] = ogg_2_wav

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
