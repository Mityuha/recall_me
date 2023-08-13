from datetime import date
from itertools import product
from random import choice
from typing import Iterator

import pytest
from recall_me.date_parser import DayTextDateParser
from recall_me.date_parser.utils import DAY_NUM_2_NAME
from recall_me.date_parser.utils import MONTH_NUM_2_NAME as MONTHS

from .constants import DATES, Faker


def generate_text_daymonth_dates(d: date) -> Iterator[tuple[str, date]]:
    month_options: list[str] = MONTHS[d.month]
    day_options: list[str] = DAY_NUM_2_NAME[d.day]

    for day_option, month_option in product(day_options, month_options):
        date_format: str
        with_year: bool
        for date_format, with_year in [
            ("{day} {month}", False),
            ("{day} {month} {year}", True),
            ("{month} {day}", False),
            ("{month} {day} {year}", True),
            ("{year} {day} {month}", True),
        ]:
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
                        day=day_option,
                        month=month_option,
                        year=f_year,
                    )
                    + " "
                    + Faker.pystr(),
                    date(year=year, month=d.month, day=d.day),
                )


def generate_any_text_daymonth_dates(
    dates: list[date],
) -> Iterator[tuple[str, list[date]]]:
    for d in dates:
        date_num: int = Faker.pyint(min_value=0, max_value=4)
        random_dates: list[date] = [d] + [choice(dates) for _ in range(date_num)]

        random_sentences: list[tuple[str, date]] = [
            choice(list(generate_text_daymonth_dates(random_date)))
            for random_date in random_dates
        ]

        sentence: str = "\n".join(s[0] for s in random_sentences)
        expected_dates: list[date] = [s[1] for s in random_sentences]

        yield (sentence, expected_dates)


@pytest.mark.parametrize("sentence, expected", generate_any_text_daymonth_dates(DATES))
def test_text_daymonth_dates(sentence: str, expected: list[date]) -> None:
    results: list[date] = DayTextDateParser().parse(sentence)
    assert set(expected) == set(results)
