import json
from dataclasses import dataclass
from typing import Any, Final

from recall_me.bot.types import AllEventsState
from sqlalchemy import delete, select  # type: ignore

from ..interfaces import Database
from ..tables import EventState


@dataclass
class State:
    callback_id: str
    user_id: str
    previous_state: AllEventsState
    current_state: AllEventsState
    metadata: Any


class StateStorage:
    def __init__(self, database: Database) -> None:
        self.database: Final[Database] = database

    async def callback_state(self, callback_id: str) -> Any:
        row = await self.database.fetch_one(
            select(EventState).where(EventState.callback_id == callback_id)
        )
        if not row:
            return None

        return State(
            callback_id=row["callback_id"],
            user_id=row["user_id"],
            previous_state=AllEventsState(row["previous_state"]),
            current_state=AllEventsState(row["current_state"]),
            metadata=row["event_metadata"],
        )

    async def save_state(
        self,
        *,
        callback_id: str,
        user_id: str,
        previous_state: AllEventsState,
        current_state: AllEventsState,
        metadata: Any
    ) -> None:
        await self.database.execute(
            """
            INSERT INTO event_state
            (callback_id, user_id, previous_state, current_state, event_metadata)
            VALUES(:callback_id, :user_id, :previous_state, """
            """:current_state, :event_metadata)
            ON CONFLICT (callback_id)
            DO UPDATE SET
            previous_state = :previous_state,
            current_state = :current_state,
            event_metadata = :event_metadata;
            """,
            values={
                "callback_id": callback_id,
                "user_id": user_id,
                "previous_state": previous_state.value,
                "current_state": current_state.value,
                "event_metadata": json.dumps(metadata),
            },
        )

    async def drop_state(self, callback_id: str) -> None:
        await self.database.execute(
            delete(EventState).where(EventState.callback_id == callback_id)
        )
