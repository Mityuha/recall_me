import re
from typing import Iterable, Protocol


class Stemmer(Protocol):
    def stem(self, word: str) -> str:
        ...


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
