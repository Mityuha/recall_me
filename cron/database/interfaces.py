from typing import Any, Protocol

from sqlalchemy.sql import ClauseElement  # type: ignore


class DatabaseAll(Protocol):
    async def fetch_all(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> list[Any]:
        ...
