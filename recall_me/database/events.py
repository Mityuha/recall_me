from dataclasses import dataclass
from datetime import time


@dataclass
class EventTable:
    id: int
    title: str
    description: str
    event_day: int
    event_month: int
    start_time: time
    duration: int
    voice_id: str
    source_text: str
    author_id: str
