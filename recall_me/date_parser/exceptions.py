from typing import Final

from .interfaces import DateParser


class DateParserError(Exception):
    ...


class AmbiguousParseResults(DateParserError):
    def __init__(
        self, *, parser1: DateParser, parser2: DateParser, sentence: str
    ) -> None:
        self.parser1: Final[DateParser] = parser1
        self.parser2: Final[DateParser] = parser2
        self.sentence: Final[str] = sentence
        super().__init__(
            f"'{parser1}' and '{parser2}' gave differerent results "
            f"for the sentence: {sentence}"
        )
