from enum import Enum, auto
from typing import Final

BACK_ARROW: Final[str] = "back"
DELETE_EVENT: Final[str] = "del"
YES: Final[str] = "1"
NO: Final[str] = "0"


class AllEventsState(Enum):
    NO_MESSAGE = auto()
    CMD_ALL_EVENTS_SCREEN = auto()
    CMD_SINGLE_EVENT_SCREEN = auto()
    CRON_NOTIFY_MESSAGE_SCREEN = auto()
    CRON_ALL_EVENTS_SCREEN = auto()
    CRON_SINGLE_EVENT_SCREEN = auto()
    #
    SAVE_EVENTS_SCREEN = auto()
