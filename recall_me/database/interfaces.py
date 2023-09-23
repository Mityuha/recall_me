from typing import Any, Protocol


class DatabaseVal(Protocol):
    async def fetch_val(self, query: str, values: dict) -> Any:
        ...
