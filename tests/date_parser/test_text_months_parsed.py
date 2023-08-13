from datetime import date
from random import choice
from typing import Final, Iterator

import pytest
from recall_me.date_parser import TextDateParser

from .constants import DATES, Faker

MONTHS: Final[dict[int, list[str]]] = {
    1: ["январь", "январю", "января", "январем", "январе", "янв.", "янвя"],
    2: ["февраль", "февралю", "февраля", "февралем", "феврале", "фев.", "фев"],
    3: ["март", "марту", "марта", "мартом", "марте"],
    4: ["апрель", "апрелю", "апреля", "апрелем", "апреле", "апр.", "апр"],
    5: ["май", "маю", "мая", "маем", "мае"],
    6: ["июнь", "июню", "июня", "июнем", "июне"],
    7: ["июль", "июлю", "июля", "июлем", "июле"],
    8: ["август", "августу", "августа", "августом", "августе", "авг.", "авг"],
    9: ["сентябрь", "сентябрю", "сентября", "сентябрем", "сентябре", "сент.", "сент"],
    10: ["октябрь", "октябрю", "октября", "октябрем", "октябре", "окт.", "окт"],
    11: ["ноябрь", "ноябрю", "ноября", "ноябрем", "ноябре", "нояб.", "нояб"],
    12: ["декабрь", "декабрю", "декабря", "декабрем", "декабре", "дек.", "дек"],
}


def generate_text_month_dates(d: date) -> Iterator[tuple[str, date]]:
    month: int = d.month
    options: list[str] = MONTHS[month]

    for option in options:
        date_format: str
        with_year: bool
        for date_format, with_year in [
            ("{day} {month}", False),
            ("{day} {month} {year}", True),
            ("{month} {day}", False),
            ("{month} {day} {year}", True),
            ("{year} {day} {month}", True),
            ("{year} {month} {day}", True),
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
                # skip 03 апреля 18
                if date_format == "{year} {month} {day}" and len(f_year) < 4:
                    continue
                yield (
                    Faker.pystr()
                    + " "
                    + date_format.format(
                        day=d.day,
                        month=option,
                        year=f_year,
                    )
                    + " "
                    + Faker.pystr(),
                    date(year=year, month=d.month, day=d.day),
                )


def generate_any_text_month_dates(
    dates: list[date],
) -> Iterator[tuple[str, list[date]]]:
    for d in dates:
        date_num: int = Faker.pyint(min_value=0, max_value=4)
        random_dates: list[date] = [d] + [choice(dates) for _ in range(date_num)]

        random_sentences: list[tuple[str, date]] = [
            choice(list(generate_text_month_dates(random_date)))
            for random_date in random_dates
        ]

        sentence: str = "\n".join(s[0] for s in random_sentences)
        expected_dates: list[date] = [s[1] for s in random_sentences]

        yield (sentence, expected_dates)


@pytest.mark.parametrize("sentence, expected", generate_any_text_month_dates(DATES))
def test_text_month_single_date(sentence: str, expected: list[date]) -> None:
    results: list[date] = TextDateParser().parse(sentence)
    assert set(expected) == set(results)
