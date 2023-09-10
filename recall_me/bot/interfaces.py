from typing import Protocol


class Ogg2WavConverter(Protocol):
    def convert(self, ogg_bytes: bytearray) -> bytes:
        ...


class TextRecognizer(Protocol):
    def recognize(self, wav_bytes: bytes) -> str:
        ...
