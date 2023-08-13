import re
from datetime import date
from typing import Final

from nltk.stem.snowball import RussianStemmer
from recall_me.logging import logger

from .interfaces import Stemmer
from .utils import DAY_NAME_2_NUM
from .utils import DAY_TEXT_R as DAY_R
from .utils import MONTH_NAME_2_NUM
from .utils import MONTH_TEXT_R as MONTH_R
from .utils import SEPARATOR_R, YEAR_R, full_year

DEFAULT_PATTERNS: Final[dict[str, str]] = {
    "day month year": f"{SEPARATOR_R}".join([DAY_R, MONTH_R, YEAR_R]),
    "month day year": f"{SEPARATOR_R}".join([MONTH_R, DAY_R, YEAR_R]),
    "year day month": f"{SEPARATOR_R}".join([YEAR_R, DAY_R, MONTH_R]),
    "year month day": f"{SEPARATOR_R}".join([YEAR_R, MONTH_R, DAY_R]),
    "day month": f"{SEPARATOR_R}".join([DAY_R, MONTH_R]),
    "month day": f"{SEPARATOR_R}".join([MONTH_R, DAY_R]),
}


class DayTextDateParser:
    def __init__(
        self,
        stemmer: Stemmer = RussianStemmer(),
        *,
        patterns: dict[str, str] | None = None,
    ) -> None:
        self.stemmer: Final[Stemmer] = stemmer
        patterns = patterns or DEFAULT_PATTERNS
        self.patterns: Final[dict[str, re.Pattern]] = {
            fmt: re.compile(pattern) for fmt, pattern in patterns.items()
        }

    def __str__(self) -> str:
        return "[DayTextDateP]"

    def parse(self, sentence: str) -> list[date]:
        sentence = sentence.replace(".", " ")
        sentence = " ".join(
            self.stemmer.stem(p.strip()) for p in sentence.split(" ") if p.strip()
        )

        logger.debug(f"{self}: parsing {sentence}")

        matches: list[date] = []

        p_format: str
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
                    return DAY_NAME_2_NUM[p[pattern_parts["day"]]]

                def month(p):
                    return MONTH_NAME_2_NUM[p[pattern_parts["month"]]]

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

                logger.debug(f"{self}: {parts} ==> {matches[-1]}")

        return matches
