from datetime import date
from typing import Any, Protocol, Sequence


class Ogg2WavConverter(Protocol):
    def convert(self, ogg_bytes: bytearray) -> bytes:
        ...


class TextRecognizer(Protocol):
    def recognize(self, wav_bytes: bytes) -> str:
        ...


class DateParser(Protocol):
    def parse(self, text: str) -> dict[str, list[date]]:
        ...


class Event(Protocol):
    title: str
    description: str
    edate: date
    start_hour: int
    duration: int


class EventFormatter(Protocol):
    def format_events(
        self,
        events: dict[str, list[date]],
    ) -> Sequence[Event]:
        ...


class EventsGetter(Protocol):
    async def __call__(self, *, update: Any, context: Any) -> Sequence[Event]:
        ...


class Event2Text(Protocol):
    def __call__(self, event: Event) -> str:
        ...


class EventsConfirmation(Protocol):
    def __call__(self, events: Sequence[Event], *, message: Any) -> None:
        ...
