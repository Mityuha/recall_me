from datetime import date
from typing import Any

from recall_me.date_parser import ComplexDateParser


def test_complex_date_parser_ok(
    mocker: Any,
    faker: Any,
    next_notification: Any,
) -> None:
    text1: str = faker.pystr()
    text2: str = faker.pystr()

    date1: date = faker.date_of_birth()
    date2: date = faker.date_of_birth()

    parser = ComplexDateParser(
        mocker.Mock(**{"parse.side_effect": [[date1], []]}),
        mocker.Mock(**{"parse.side_effect": [[], [date2]]}),
    )

    text = f"{text1}\n{text2}"

    results: dict[str, list[date]] = parser.parse(text)

    assert results[text1] == [next_notification(date1)]
    assert results[text2] == [next_notification(date2)]
