from typing import Protocol


class SmartTitleI(Protocol):
    def __call__(self, title: str) -> str:
        ...
