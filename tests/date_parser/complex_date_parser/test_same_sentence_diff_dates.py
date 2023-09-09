from datetime import date
from typing import Any

import pytest
from recall_me.date_parser import ComplexDateParser
from recall_me.date_parser.exceptions import AmbiguousParseResults


def test_complex_date_parser_ok(
    mocker: Any,
    faker: Any,
) -> None:
    date1: date = faker.date_of_birth()
    date2: date = faker.date_of_birth()

    parser = ComplexDateParser(
        mocker.Mock(**{"parse.side_effect": [[date1]]}),
        mocker.Mock(**{"parse.side_effect": [[date2]]}),
    )

    text: str = faker.pystr()

    with pytest.raises(AmbiguousParseResults):
        parser.parse(text)
