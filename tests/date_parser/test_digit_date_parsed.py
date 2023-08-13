from datetime import date
from random import choice
from typing import Callable, Final, Iterator

import pytest
from faker import Faker as FakerType
from recall_me.date_parser import DigitDateParser

Faker = FakerType()

DATES: Final[list[date]] = [
    date(2023, 8, 26),
    date(1990, 10, 6),
    date(1991, 3, 4),
    date(1992, 2, 10),
    date(1991, 2, 7),
    date(1997, 1, 30),
    date(2003, 4, 18),
    date(1992, 6, 3),
    date(2003, 6, 21),
    date(1995, 7, 28),
    date(1997, 11, 19),
    date(1992, 12, 11),
    date(1993, 2, 17),
    date(2003, 3, 29),
    date(1998, 3, 26),
    date(1999, 8, 27),
    date(2000, 4, 5),
    date(1996, 8, 12),
    date(2006, 6, 6),
    date(1973, 5, 1),
    date(1988, 12, 13),
    date(1989, 10, 28),
    date(1987, 1, 20),
    date(1988, 2, 19),
    date(1999, 12, 27),
    date(2010, 1, 16),
    date(2022, 2, 22),
]

PRETTY_FORMAT: Final[dict[str, Callable[[date], int]]] = {
    "day": lambda d: d.day,
    "month": lambda d: d.month,
    "year": lambda d: d.year,
}


def format_with_any_text(
    d: date,
    date_format: str,
    separator: str,
) -> str:
    formatters: list[Callable] = [PRETTY_FORMAT[fmt] for fmt in date_format.split(" ")]
    values: list[str] = [str(fmt(d)) for fmt in formatters]
    separated_values: str = f"{separator}".join(values)
    return Faker.pystr() + " " + separated_values + " " + Faker.pystr()


def single_date_sentences(d: date) -> Iterator[tuple[str, date]]:
    for separator in r"./ \|":
        for date_format, with_year in (
            ("day month", False),
            ("day month year", True),
        ):
            expected_date = d
            if not with_year:
                expected_date = date(date.today().year, d.month, d.day)
                if expected_date < date.today():
                    expected_date = date(date.today().year + 1, d.month, d.day)
            yield (
                format_with_any_text(
                    d,
                    date_format=date_format,
                    separator=separator,
                ),
                expected_date,
            )


def generate_single_date_sentences(dates: list[date]) -> Iterator[tuple[str, date]]:
    for d in dates:
        yield from single_date_sentences(d)


def generate_any_date_sentences(dates: list[date]) -> Iterator[tuple[str, list[date]]]:
    for d in dates:
        date_num: int = Faker.pyint(min_value=1, max_value=4)
        random_dates: list[date] = [d] + [choice(dates) for _ in range(date_num)]

        random_sentences: list[tuple[str, date]] = [
            choice(list(single_date_sentences(random_date)))
            for random_date in random_dates
        ]

        sentence: str = "\n".join(s[0] for s in random_sentences)
        expected_dates: list[date] = [s[1] for s in random_sentences]

        yield (sentence, expected_dates)


@pytest.mark.parametrize(
    "sentence, expected",
    generate_single_date_sentences(DATES),
)
def test_parse_single_date(sentence: str, expected: date) -> None:
    results: list[date] = DigitDateParser().parse(sentence)
    assert [expected] == results


@pytest.mark.parametrize(
    "sentence, expected",
    generate_any_date_sentences(DATES),
)
def test_parse_any_dates(sentence: str, expected: list[date]) -> None:
    results: list[date] = DigitDateParser().parse(sentence)
    assert set(expected) == set(results)
