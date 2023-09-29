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


class TextEditor(Protocol):
    async def edit_message_text(self, text: str) -> Any:
        ...


class EventsConfirmation(Protocol):
    async def send_confirmation(
        self, events: Sequence[Event], *, message: Any
    ) -> tuple[bool, TextEditor]:
        ...


class EventSaver(Protocol):
    async def save_event(
        self,
        *,
        title: str,
        description: str,
        event_day: int,
        event_month: int,
        voice_id: str | None,
        source_text: str | None,
        author_id: str,
        duration: int = 2,
        start_hour: int = -1,
        notify_before_days: int = 7,
    ) -> None:
        ...


class Storage(Protocol):
    async def callback_metadata(
        self,
        callback_id: str,
    ) -> Any | None:
        ...


class Router(Protocol):
    async def route_callback(
        self,
        callback_id: str,
        callback_data: str,
        callback_metadata: Any,
        query: Any,
    ) -> None:
        ...
