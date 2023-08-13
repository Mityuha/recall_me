import re
from datetime import date
from typing import Final

from recall_me.logging import logger

from .utils import DAY_R, MONTH_R, SEPARATOR_R, YEAR_R, full_year

# Important note: sort patterns by length's descending order
DEFAULT_PATTERNS: Final[dict[str, str]] = {
    "day month year": f"{SEPARATOR_R}".join([DAY_R, MONTH_R, YEAR_R]),
    "day month": f"{SEPARATOR_R}".join([DAY_R, MONTH_R]),
}


class DigitDateParser:
    def __init__(
        self,
        *,
        patterns: dict[str, str] | None = None,
    ) -> None:
        patterns = patterns or DEFAULT_PATTERNS
        self.patterns: Final[dict[str, re.Pattern]] = {
            fmt: re.compile(pattern) for fmt, pattern in patterns.items()
        }

    def __str__(self) -> str:
        return "[DigitDateP]"

    def parse(self, sentence: str) -> list[date]:
        sentence = sentence.replace("\\", "/")

        logger.debug(f"{self}: parsing {sentence}")

        matches: list[date] = []
        pattern: re.Pattern
        for p_format, pattern in self.patterns.items():
            logger.debug(f"{self}: check against pattern {p_format}")
            date_matches: list[tuple] = pattern.findall(sentence)

            if not date_matches:
                continue

            logger.debug(f"{self}: matches are found: {date_matches}")

            sentence = pattern.sub("", sentence)
            logger.debug(f"{self}: sentence after pattern replacing: '{sentence}'")

            for date_match in date_matches:
                parts: tuple = date_match
                logger.debug(f"{self}: parts of the Match obj: {parts}")
                pattern_parts: dict[str, int] = {
                    part: index for index, part in enumerate(p_format.split(" "))
                }
                assert len(parts) == len(pattern_parts), (parts, pattern_parts)

                def day(p):
                    return int(p[pattern_parts["day"]])

                def month(p):
                    return int(p[pattern_parts["month"]])

                def year(p):
                    return full_year(int(p[pattern_parts["year"]]))

                if len(parts) == 3:
                    matches.append(
                        date(
                            day=day(parts),
                            month=month(parts),
                            year=year(parts),
                        )
                    )
                elif len(parts) == 2:
                    parsed_date: date = date(
                        day=day(parts),
                        month=month(parts),
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
