from typing import Final

from .interfaces import DatabaseExec


class DeleteEvent:
    def __init__(self, database: DatabaseExec) -> None:
        self.database: Final[DatabaseExec] = database

    async def delete_event(
        self,
        event_id: str | int,
    ) -> None:
        await self.database.execute(
            "DELETE FROM event " "WHERE id=:event_id;",
            {"event_id": int(event_id)},
        )
