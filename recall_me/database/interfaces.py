from typing import Any, Protocol

from sqlalchemy.sql import ClauseElement


class DatabaseVal(Protocol):
    async def fetch_val(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> Any:
        ...


class DatabaseAll(Protocol):
    async def fetch_all(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> list[Any]:
        ...


class DatabaseOne(Protocol):
    async def fetch_one(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> Any:
        ...


class DatabaseExec(Protocol):
    async def execute(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> Any:
        ...


class Database(Protocol):
    async def fetch_val(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> Any:
        ...

    async def fetch_all(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> list[Any]:
        ...

    async def fetch_one(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> Any:
        ...

    async def execute(
        self, query: str | ClauseElement, values: dict | None = None
    ) -> Any:
        ...
