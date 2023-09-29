from enum import Enum, auto
from typing import Final

BACK_ARROW: Final[str] = "back"
DELETE_EVENT: Final[str] = "del"


class AllEventsState(Enum):
    NO_MESSAGE = auto()
    CRON_SHOW_EVENTS_BUTTON_SCREEN = auto()
    CRON_ALL_EVENTS_SCREEN = auto()
    CMD_ALL_EVENTS_SCREEN = auto()
    SINGLE_EVENT_SCREEN = auto()
