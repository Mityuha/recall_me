from dataclasses import dataclass
from datetime import date


@dataclass
class Event:
    title: str
    description: str
    edate: date
    start_hour: int = -1
    duration: int = 2
