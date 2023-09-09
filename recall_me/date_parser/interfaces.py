import re
from datetime import date
from typing import Iterable, Protocol


class DateStrategy(Protocol):
    def prepare_sentence(self, sentence: str) -> str:
        ...

    def patterns(self) -> Iterable[re.Pattern]:
        ...

    def day(self, parts: tuple) -> int:
        ...

    def month(self, parts: tuple) -> int:
        ...

    def year(self, parts: tuple) -> int:
        ...


class DateParser(Protocol):
    def parse(self, sentence: str) -> list[date]:
        ...
