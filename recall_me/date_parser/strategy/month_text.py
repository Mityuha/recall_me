import re
from typing import Final

from nltk.stem.snowball import RussianStemmer  # type: ignore

from .interfaces import Stemmer
from .patterns import PatternsMixin
from .utils import DAY_R, MONTH_NAME_2_NUM
from .utils import MONTH_TEXT_R as MONTH_R
from .utils import SEPARATOR_R, YEAR_R, full_year

DEFAULT_PATTERNS: Final[dict[str, str]] = {
    "day month year": f"{SEPARATOR_R}".join([DAY_R, MONTH_R, YEAR_R]),
    "month day year": f"{SEPARATOR_R}".join([MONTH_R, DAY_R, YEAR_R]),
    "year day month": f"{SEPARATOR_R}".join([YEAR_R, DAY_R, MONTH_R]),
    "year month day": f"{SEPARATOR_R}".join([YEAR_R, MONTH_R, DAY_R]),
    "day month": f"{SEPARATOR_R}".join([DAY_R, MONTH_R]),
    "month day": f"{SEPARATOR_R}".join([MONTH_R, DAY_R]),
}


class MonthTextStrategy(PatternsMixin):
    def __init__(
        self,
        stemmer: Stemmer = RussianStemmer(),
        *,
        patterns: dict[str, str] | None = None,
    ) -> None:
        self.stemmer: Final[Stemmer] = stemmer
        patterns = patterns or DEFAULT_PATTERNS
        super().__init__(
            {fmt: re.compile(pattern) for fmt, pattern in patterns.items()}
        )

    def __str__(self) -> str:
        return "[TextMonth]"

    def prepare_sentence(self, sentence: str) -> str:
        sentence = sentence.replace(".", " ")
        return " ".join(
            self.stemmer.stem(p.strip()) for p in sentence.split(" ") if p.strip()
        )

    def day(self, p: tuple) -> int:
        self._check_parts(p)
        return int(p[self._pattern_parts["day"]])

    def month(self, p: tuple) -> int:
        self._check_parts(p)
        return MONTH_NAME_2_NUM[p[self._pattern_parts["month"]]]

    def year(self, p: tuple) -> int:
        self._check_parts(p)
        return full_year(int(p[self._pattern_parts["year"]]))
