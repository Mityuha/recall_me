from typing import Any, Protocol


class DatabaseVal(Protocol):
    async def fetch_val(self, query: str, values: dict) -> Any:
        ...


class DatabaseAll(Protocol):
    async def fetch_all(self, query: str, values: dict) -> list[Any]:
        ...


class DatabaseOne(Protocol):
    async def fetch_one(self, query: str, values: dict) -> Any:
        ...


class DatabaseExec(Protocol):
    async def execute(self, query: str, values: dict) -> Any:
        ...
