from datetime import date
from typing import Any

import pytest
from recall_me.date_parser import Event, EventFormatter


def test_event_formatter_simple(mocker: Any, faker: Any) -> None:
    random_date: date = faker.date_of_birth()
    dates = [random_date.replace(day=i) for i in range(1, 22)]
    step = 7
    raw_events: dict[str, list[date]] = {
        faker.pystr(): dates[step * (i - 1) : step * i] for i in range(1, 4)
    }

    formatter: EventFormatter = EventFormatter(lambda x: x)

    events: list[Event] = formatter.format_events(raw_events)

    for event, edates in raw_events.items():
        for edate in edates:
            for e in events:
                if e.description == event and e.edate == edate:
                    break
            else:
                assert False, f"Event {event} with date {edate} wasn't formatted."


@pytest.mark.parametrize(
    "enumber",
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 26, 28, 30],
)
def test_lot_of_events_in_one_date(
    mocker: Any,
    faker: Any,
    enumber: int,
) -> None:
    edate = faker.date_of_birth()
    raw_events = {faker.pystr(): [edate] for _ in range(enumber)}

    formatter: EventFormatter = EventFormatter(lambda x: x)

    events: list[Event] = formatter.format_events(raw_events)

    for event in raw_events:
        for e in events:
            assert e.edate == edate
            if e.description == event:
                print(e.edate, e.start_hour)
                break
        else:
            assert False, f"Event {event} wasn't formatted"
