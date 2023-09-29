from typing import Any


class Storage:
    def __init__(self) -> None:
        ...

    async def __aenter__(self) -> "Storage":
        return self

    async def __aexit__(self, *_args: Any) -> None:
        return None

    async def callback_received(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: Any,
    ) -> None:
        ...

    def __contains__(self, item: Any) -> bool:
        ...
