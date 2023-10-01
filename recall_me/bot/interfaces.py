from datetime import date
from typing import Any, Protocol


class EventInfo(Protocol):
    eid: int
    title: str
    description: str
    edate: date
    voice_id: str
    start_hour: int
    duration: int


class Storage(Protocol):
    async def callback_state(
        self,
        callback_id: str,
    ) -> Any | None:
        ...


class Router(Protocol):
    async def route_callback(
        self,
        *,
        callback_id: str,
        callback_data: str,
        callback_state: Any,
        query: Any,
    ) -> None:
        ...
