from typing import Protocol

from ..types import BACK_ARROW, DELETE_EVENT, AllEventsState  # noqa


class CallbackMetadata(Protocol):
    user_id: str
    message_id: int
    state: AllEventsState
