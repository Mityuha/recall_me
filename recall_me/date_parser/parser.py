import re
from datetime import date
from typing import Final

from ..logging import logger
from .interfaces import DateStrategy


def create_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year=year, month=month, day=day)
    except ValueError as exc:
        logger.info(f"Date {year}-{month}-{day} is invalid: {exc}")

    return None


class DateParser:
    def __init__(
        self,
        strategy: DateStrategy,
    ) -> None:
        self.strategy: Final[DateStrategy] = strategy

    def __str__(self) -> str:
        return f"{self.strategy}"

    def parse(self, sentence: str) -> list[date]:
        sentence = self.strategy.prepare_sentence(sentence)

        logger.debug(f"{self}: parsing {sentence}")

        matches: list[date] = []

        pattern: re.Pattern
        for pattern in self.strategy.patterns():
            date_matches: list[tuple] = pattern.findall(sentence)

            if not date_matches:
                continue

            logger.debug(f"{self}: matches are found: {date_matches}")

            sentence = pattern.sub("", sentence)
            logger.debug(f"{self}: sentence after pattern replacing: '{sentence}'")
            for date_match in date_matches:
                parts: tuple = date_match
                logger.debug(f"{self}: parts of the Match obj: {parts}")

                parsed_date: date | None
                if len(parts) == 3:
                    parsed_date = create_date(
                        day=self.strategy.day(parts),
                        month=self.strategy.month(parts),
                        year=self.strategy.year(parts),
                    )
                    if parsed_date:
                        matches.append(parsed_date)
                elif len(parts) == 2:
                    parsed_date = create_date(
                        day=self.strategy.day(parts),
                        month=self.strategy.month(parts),
                        year=date.today().year,
                    )
                    if parsed_date and (parsed_date < date.today()):
                        parsed_date = create_date(
                            year=parsed_date.year + 1,
                            month=parsed_date.month,
                            day=parsed_date.day,
                        )

                    if parsed_date:
                        matches.append(parsed_date)

                if matches:
                    logger.debug(f"{self}: {parts} ==> {matches[-1]}")

        return matches
