from datetime import date
from typing import Final

MONTH_NUM_2_NAME: Final[dict[int, set[str]]] = {
    1: {"янв", "январ"},
    2: {"фев", "феврал"},
    3: {"март"},
    4: {"апр", "апрел"},
    5: {"ма"},
    6: {"июн"},
    7: {"июл"},
    8: {"авг", "август"},
    9: {"сент", "сентябр"},
    10: {"окт", "октябр"},
    11: {"нояб", "ноябр"},
    12: {"дек", "декабр"},
}

MONTH_NAME_2_NUM: Final[dict[str, int]] = {
    word: num for num, words in MONTH_NUM_2_NAME.items() for word in words
}

SEPARATOR: Final[str] = r" /|.-"
SEPARATOR_R: Final[str] = f"[{SEPARATOR}]"
DAY_R: Final[str] = r"\b(3[01]|[12][0-9]|0?[1-9])\b"
MONTH_R: Final[str] = r"\b(1[0-2]|0?[1-9])\b"
YEAR_R: Final[str] = r"\b((?:19|20)?[0-9]{2})\b"
MONTH_TEXT_R: Final[str] = r"\b(" + r"|".join(MONTH_NAME_2_NUM) + r")\b"


def full_year(year: int) -> int:
    if year > 100:  # 4 digits
        return year

    cur_year: int = date.today().year
    cur_year_2_digits: int = cur_year % 1000 % 100

    if year <= cur_year_2_digits:
        return (cur_year - cur_year_2_digits) + year

    return (cur_year - cur_year_2_digits - 100) + year
