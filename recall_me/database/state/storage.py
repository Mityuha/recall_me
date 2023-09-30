from dataclasses import dataclass
from typing import Any

from recall_me.bot.types import AllEventsState


@dataclass
class State:
    callback_id: str
    user_id: str
    previous_state: AllEventsState
    current_state: AllEventsState
    metadata: Any


class StateStorage:
    def __init__(self) -> None:
        self.storage: list[State] = []

    async def callback_metadata(self, callback_id: str) -> Any:
        for state in self.storage:
            if state.callback_id == callback_id:
                return state

        return None

    async def save_state(
        self,
        *,
        callback_id: str,
        user_id: str,
        previous_state: AllEventsState,
        current_state: AllEventsState,
        metadata: Any
    ) -> None:
        for state in self.storage:
            if state.callback_id == callback_id:
                state.previous_state = previous_state
                state.current_state = current_state
                state.metadata = metadata

        else:
            self.storage.append(
                State(
                    callback_id=callback_id,
                    user_id=user_id,
                    previous_state=previous_state,
                    current_state=current_state,
                    metadata=metadata,
                )
            )
