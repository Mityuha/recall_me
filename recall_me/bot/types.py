from enum import Enum
from typing import Final

BACK_ARROW: Final[str] = "back"
DELETE_EVENT: Final[str] = "del"
YES: Final[str] = "1"
NO: Final[str] = "0"


class AllEventsState(Enum):
    NO_MESSAGE = 0
    CMD_ALL_EVENTS_SCREEN = 1
    CMD_SINGLE_EVENT_SCREEN = 2
    CRON_NOTIFY_MESSAGE_SCREEN = 3
    CRON_ALL_EVENTS_SCREEN = 4
    CRON_SINGLE_EVENT_SCREEN = 5
    #
    SAVE_EVENTS_SCREEN = 6
