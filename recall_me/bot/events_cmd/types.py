from enum import Enum, auto
from typing import Final

BACK_ARROW: Final[str] = "back"
DELETE_EVENT: Final[str] = "del"


class AllEventsState(Enum):
    ALL_EVENTS_SCREEN = auto()
    SINGLE_EVENT_SCREEN = auto()
