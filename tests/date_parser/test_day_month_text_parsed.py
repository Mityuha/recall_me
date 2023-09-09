from datetime import date
from itertools import product
from random import choice
from typing import Iterator

import pytest
from recall_me.date_parser import DAY_NUM_2_NAME
from recall_me.date_parser import MONTH_NUM_2_NAME as MONTHS
from recall_me.date_parser import DateParser, DayMonthTextStrategy

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
    results: list[date] = DateParser(DayMonthTextStrategy()).parse(sentence)
    assert set(expected) == set(results)


@pytest.mark.parametrize(
    "sentence, expected",
    (
        ("двадцать шестого августа в субботу", date(2023, 8, 26)),
        ("шестого октября макс володин", date(2023, 10, 6)),
        ("четвёртого марта дэн", date(2023, 3, 4)),
        ("десятого февраля хорошо", date(2023, 2, 10)),
        ("седьмого февраля лерка", date(2023, 2, 7)),
        ("тридцатого января кальян колян", date(2023, 1, 30)),
        ("восемнадцатого апреля саша сестричка", date(2023, 4, 18)),
        ("третьего июля артём соловейчик", date(2023, 7, 3)),
        ("никита двадцать первого июня", date(2023, 6, 21)),
        ("двадцать восьмого июля антоху парфенов", date(2023, 7, 28)),
        ("девятнадцатого ноября анечка", date(2023, 11, 19)),
        ("одиннадцатого декабря лёг сорочки", date(2023, 12, 11)),
        ("семнадцатого февраля антон хорошо", date(2023, 2, 17)),
        ("двадцать девятого марта юлька сашина", date(2023, 3, 29)),
        ("двадцать шестого марта андрюха сашин", date(2023, 3, 26)),
        ("двадцать седьмое августа насте володина", date(2023, 8, 27)),
        ("пятое апреля на стаж оконного", date(2023, 4, 5)),
        ("пятое апреля наташа конного", date(2023, 4, 5)),
        ("двенадцатая августа лёха григорьев", date(2023, 8, 12)),
        ("шестое июня игорь капралов", date(2023, 6, 6)),
        ("первое мая игорь евгеньевич", date(2023, 5, 1)),
        ("тринадцатый декабря сани лукин", date(2023, 12, 13)),
        ("двадцать восьмой октября мстислав", date(2023, 10, 28)),
        ("ванька двадцатого января", date(2023, 1, 20)),
        ("орешка девятнадцатого февраля", date(2023, 2, 19)),
        ("двадцать седьмое декабря дима хлопков", date(2023, 12, 27)),
        ("шестнадцатая января крестная", date(2023, 1, 16)),
        ("иди двадцать второе февраля демон галкин", date(2023, 2, 22)),
        ("второго февраля андрюха парфенов", date(2023, 2, 2)),
        ("седьмое февраля митяй", date(2023, 2, 7)),
    ),
)
def test_text_daymonth_extra(sentence: str, expected: date) -> None:
    results: list[date] = DateParser(DayMonthTextStrategy()).parse(sentence)
    assert len(results) == 1
    assert results[0].month == expected.month
    assert results[0].day == expected.day
