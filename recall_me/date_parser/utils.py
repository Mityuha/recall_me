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
DAY_R: Final[str] = "(3[01]|[12][0-9]|0?[1-9])"
MONTH_R: Final[str] = "(1[0-2]|0?[1-9])"
YEAR_R: Final[str] = "((?:[0-9]{2})[0-9]{2})"
MONTH_TEXT_R: Final[str] = "(" + "|".join(MONTH_NAME_2_NUM) + ")"
