from collections import defaultdict
from datetime import date
from typing import Final, Sequence

from .interfaces import TitleMaker
from .types import Event


class EventFormatter:
    def __init__(self, title_maker: TitleMaker) -> None:
        self.title_maker: Final[TitleMaker] = title_maker

    @staticmethod
    def _date_hours_grid(enumber: int) -> Sequence[int]:
        hours = list(range(8, 22)) * 3
        if enumber <= 10:
            hours = [8, 10, 12, 14, 16] * 2
        elif enumber <= 14:
            hours = [8, 10, 12, 14, 16, 18, 20] * 2

        if len(hours) < enumber:
            assert False, f"too many events ({enumber}) for single date"

        return [hours[i] for i in range(enumber)]

    def format_events(self, events: dict[str, list[date]]) -> list[Event]:
        d2e = defaultdict(list)
        event: str
        edate: date

        for event, dates in events.items():
            for edate in dates:
                d2e[edate].append(event)

        result: list[Event] = []
        for edate, etexts in d2e.items():
            hours_grid: Sequence[int] = self._date_hours_grid(len(etexts))

            assert len(etexts) == len(hours_grid), (len(etexts), len(hours_grid))
            for text, hour in zip(etexts, hours_grid):
                result.append(
                    Event(
                        title=self.title_maker(text),
                        description=text,
                        edate=edate,
                        start_hour=hour,
                    )
                )

        return result
