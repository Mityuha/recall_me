import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final
from zipfile import ZipFile

from recall_me.logging import logger
from vosk import KaldiRecognizer, Model  # type: ignore


class TextRecognizer:
    def __init__(self, model_path: Path, *, framerate: int) -> None:
        zip_model = ZipFile(model_path)
        with TemporaryDirectory() as tempdir:
            zip_model.extractall(tempdir)

            model = Model(str(Path(tempdir) / model_path.stem))

        self.reco: Final[KaldiRecognizer] = KaldiRecognizer(model, framerate)

    def __str__(self) -> str:
        return "[TextRecognizer]"

    def recognize(self, wav_bytes: bytes) -> str:
        self.reco.AcceptWaveform(wav_bytes)
        data: str = (
            self.reco.Result() or self.reco.PartialResult() or self.reco.FinalResult()
        )

        logger.debug(f"{self}: parsed data: {data}")
        result: dict = json.loads(data)
        text: str = result.get("text", "") or result.get("partial", "")
        logger.debug(f"{self}: parsed text: {text}")
        return text
