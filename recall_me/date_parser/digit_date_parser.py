import re
from datetime import date
from typing import Final

from recall_me.logging import logger

SEPARATOR: Final[str] = r" /|.-"
SEPARATOR_R: Final[str] = f"[{SEPARATOR}]"
DAY_R: Final[str] = "(3[01]|[12][0-9]|0?[1-9])"
MONTH_R: Final[str] = "(1[0-2]|0?[1-9])"
YEAR_R: Final[str] = "((?:[0-9]{2})[0-9]{2})"

# Important note: sort patterns by length's descending order
DEFAULT_PATTERNS: Final[list[str]] = [
    f"{DAY_R}{SEPARATOR_R}{MONTH_R}{SEPARATOR_R}{YEAR_R}",
    f"{DAY_R}{SEPARATOR_R}{MONTH_R}",
]


class DigitDateParser:
    def __init__(
        self,
        *,
        patterns: list[str] | None = None,
    ) -> None:
        patterns = patterns or DEFAULT_PATTERNS
        self.patterns: Final[list[re.Pattern]] = [
            re.compile(pattern) for pattern in patterns
        ]

    def __str__(self) -> str:
        return "[DigitDateP]"

    def parse(self, sentence: str) -> list[date]:
        pattern: re.Pattern

        sentence = sentence.replace("\\", "/")

        logger.debug(f"{self}: parsing {sentence}")

        matches: list[date] = []
        for pattern in self.patterns:
            logger.debug(f"{self}: check against pattern {pattern}")
            date_matches: list[tuple] = pattern.findall(sentence)

            if not date_matches:
                continue

            logger.debug(f"{self}: matches are found: {date_matches}")

            sentence = pattern.sub("", sentence)
            logger.debug(f"{self}: sentence after pattern replacing: '{sentence}'")

            for date_match in date_matches:
                parts: tuple = date_match
                logger.debug(f"{self}: parts of the Match obj: {parts}")
                assert 1 < len(parts) < 4
                if len(parts) == 3:
                    matches.append(
                        date(
                            day=int(parts[0]),
                            month=int(parts[1]),
                            year=int(parts[2]),
                        )
                    )
                elif len(parts) == 2:
                    parsed_date: date = date(
                        day=int(parts[0]),
                        month=int(parts[1]),
                        year=date.today().year,
                    )
                    if parsed_date < date.today():
                        parsed_date = date(
                            year=parsed_date.year + 1,
                            month=parsed_date.month,
                            day=parsed_date.day,
                        )

                    matches.append(parsed_date)

                logger.debug(f"{self}: {parts} translated into object: {matches[-1]}")

        return matches
