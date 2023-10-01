from dataclasses import dataclass
from datetime import date


@dataclass
class Event:
    eid: int
    title: str
    description: str
    edate: date
    voice_id: str
    start_hour: int
    duration: int
