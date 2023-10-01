from calendar_view.config import style  # type: ignore
from calendar_view.core.event import EventStyle  # type: ignore

TRANSPARENT = EventStyle(event_border=(0, 0, 0, 0), event_fill=(0, 0, 0, 0))

style.hour_height = 128
