import json
from typing import Any, Final

from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes


class VoiceHandler:
    def __init__(
        self,
        voice_2_text: Any,
        *,
        ogg_2_wav: Any,
    ) -> None:
        self.voice_2_text: Final = voice_2_text
        self.ogg_2_wav: Final = ogg_2_wav

    def __str__(self) -> str:
        return "[VoiceHandler]"

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not update.message or not update.message.voice:
            return

        # get basic info about the voice note file and prepare it for downloading
        new_file = await context.bot.get_file(update.message.voice.file_id)
        # download the voice note as a file
        ogg_bytes: bytearray = await new_file.download_as_bytearray()

        logger.debug(f"{self}: ogg file received ({len(ogg_bytes)} bytes)")

        wav_bytes: bytes = self.ogg_2_wav.convert(ogg_bytes)

        self.voice_2_text.AcceptWaveform(wav_bytes)
        data: str = (
            self.voice_2_text.Result()
            or self.voice_2_text.PartialResult()
            or self.voice_2_text.FinalResult()
        )

        logger.debug(f"{self}: parsed data: {data}")
        result: dict = json.loads(data)
        text: str = result.get("text", "") or result.get("partial", "")
        logger.debug(f"Parsed text: {text}")
