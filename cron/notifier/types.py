from dataclasses import dataclass
from datetime import date

from calendar_view.core.event import EventStyle  # type: ignore
from calendar_view.core.event import EventStyles  # type: ignore

TRANSPARENT = EventStyle(
    event_border=(0, 0, 0, 0),
    event_fill=(0, 0, 0, 0),
)
PALE_PINK = EventStyle(
    event_border=(255, 20, 147, 240),
    event_fill=(253, 224, 217, 180),
)
WATER = EventStyle(
    event_border=(0, 191, 255, 240),
    event_fill=(202, 244, 244, 180),
)
BLANCHED_ALMOLD = EventStyle(
    event_border=(255, 127, 80, 240),
    event_fill=(255, 242, 204, 180),
)
TEA_GREEN = EventStyle(
    event_border=(120, 180, 120, 240),
    event_fill=(202, 239, 209, 180),
)
IVORY = EventStyle(
    event_border=(200, 200, 180, 240),
    event_fill=(252, 255, 233, 180),
)

GRAY = EventStyles.GRAY


@dataclass
class Event:
    edate: date
    description: str = ""
    title: str = ""
    start_hour: int = 10
    duration: int = 2
    style: EventStyles = EventStyles.GREEN
