from datetime import date
from random import choice
from typing import Iterator

import pytest
from faker import Faker as FakerType
from recall_me.date_parser import DigitDateParser

from .constants import DATES

Faker = FakerType()


def single_date_sentences(d: date) -> Iterator[tuple[str, date]]:
    separators = r"./ \|"
    sep_1 = choice(separators)
    sep_2 = choice(separators)
    for date_format, with_year in (
        ("{day}{separator1}{month}", False),
        ("{day}{separator1}{month}{separator2}{year}", True),
    ):
        year: int = d.year
        if not with_year:
            year = date.today().year
            if date(year, d.month, d.day) < date.today():
                year += 1

        year_2d: int = d.year % 1000 % 100
        formatted_year_2d: str = str(year_2d)
        if year_2d < 10:
            formatted_year_2d = f"0{year_2d}"

        for f_year in (str(year), formatted_year_2d):
            yield (
                Faker.pystr()
                + " "
                + date_format.format(
                    day=d.day,
                    month=d.month,
                    year=f_year,
                    separator1=sep_1,
                    separator2=sep_2,
                )
                + " "
                + Faker.pystr(),
                date(year=year, month=d.month, day=d.day),
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
