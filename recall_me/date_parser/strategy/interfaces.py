from typing import Protocol


class Stemmer(Protocol):
    def stem(self, word: str) -> str:
        ...
