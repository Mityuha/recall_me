from typing import Final, Iterable

from .interfaces import DatabaseAll


class BotUsers:
    def __init__(self, database: DatabaseAll) -> None:
        self.database: Final[DatabaseAll] = database

    async def get_bot_users(
        self,
    ) -> Iterable[str]:
        rows = await self.database.fetch_all("SELECT DISTINCT author_id FROM event;")

        return [r["author_id"] for r in rows]
