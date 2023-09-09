from datetime import date
from typing import Any

from recall_me.date_parser import ComplexDateParser


def test_complex_date_parser_the_same_date(
    mocker: Any,
    faker: Any,
    next_notification: Any,
) -> None:
    date1: date = faker.date_of_birth()
    date2: date = faker.date_of_birth()

    date11: date = date1.replace(year=1982)
    date22: date = date2.replace(year=1822)

    parser = ComplexDateParser(
        mocker.Mock(**{"parse.side_effect": [[date1, date2]]}),
        mocker.Mock(**{"parse.side_effect": [[date11, date22]]}),
        mocker.Mock(**{"parse.side_effect": [[date1, date22]]}),
        mocker.Mock(**{"parse.side_effect": [[date2, date11]]}),
        mocker.Mock(**{"parse.side_effect": [[date22, date1]]}),
    )

    text: str = faker.pystr()
    results: dict[str, list[date]] = parser.parse(text)

    assert set(results[text]) == {next_notification(date1), next_notification(date2)}
