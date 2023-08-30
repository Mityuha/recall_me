import wave
from io import BytesIO
from typing import Callable, Final

import ffmpeg
from recall_me.logging import logger


class Ogg2WavConverter:
    def __init__(self, framerate: int = 16000) -> None:
        self.framerate: Final[int] = framerate
        self.converter_factory: Callable = lambda: (
            ffmpeg.input("pipe:", format="ogg")
            .output("pipe:", format="wav", ar=framerate, ac=1)
            .run_async(pipe_stdin=True, pipe_stdout=True)
        )

    def __str__(self) -> str:
        return "[Ogg2Wav]"

    def convert(self, ogg_bytearray: bytearray) -> bytes:
        ffmpeg_process = self.converter_factory()
        wav_bytes: bytes
        with ffmpeg_process:
            wav_bytes, _ = ffmpeg_process.communicate(bytes(ogg_bytearray))

        logger.debug(f"{self}: wav buffer size: {len(wav_bytes)} bytes")
        wav_file: BytesIO = BytesIO(wav_bytes)
        wf: wave.Wave_read = wave.open(wav_file, "rb")

        if (
            wf.getnchannels() != 1
            or wf.getsampwidth() != 2
            or wf.getcomptype() != "NONE"
            or wf.getframerate() != self.framerate
        ):
            logger.error(
                "Audio file must be WAV format mono PCM.",
                f"{wf.getnchannels() = }, "
                f"{wf.getsampwidth() = }, "
                f"{wf.getcomptype() = }, ",
                f"{wf.getframerate() = }",
            )

        return wf.readframes(wf.getnframes())
