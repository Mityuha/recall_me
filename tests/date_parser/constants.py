from datetime import date
from typing import Final

from faker import Faker as FakerType

Faker: Final[FakerType] = FakerType()

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
