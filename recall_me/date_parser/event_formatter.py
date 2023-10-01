from collections import defaultdict
from datetime import date
from typing import Final

from .interfaces import TitleMaker
from .types import Event


class EventFormatter:
    def __init__(self, title_maker: TitleMaker) -> None:
        self.title_maker: Final[TitleMaker] = title_maker

    def format_events(self, events: dict[str, list[date]]) -> list[Event]:
        d2e = defaultdict(list)
        event: str
        edate: date

        for event, dates in events.items():
            for edate in dates:
                d2e[edate].append(event)

        result: list[Event] = []
        for edate, etexts in d2e.items():
            for text in etexts:
                result.append(
                    Event(
                        title=self.title_maker(text),
                        description=text,
                        edate=edate,
                    )
                )

        return result
