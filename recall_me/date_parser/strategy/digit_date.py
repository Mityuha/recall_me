import re
from typing import Final

from .patterns import PatternsMixin
from .utils import DAY_R, MONTH_R, SEPARATOR_R, YEAR_R, full_year

# Important note: sort patterns by length's descending order
DEFAULT_PATTERNS: Final[dict[str, str]] = {
    "day month year": f"{SEPARATOR_R}".join([DAY_R, MONTH_R, YEAR_R]),
    "day month": f"{SEPARATOR_R}".join([DAY_R, MONTH_R]),
}


class DigitDateStrategy(PatternsMixin):
    def __init__(
        self,
        *,
        patterns: dict[str, str] | None = None,
    ) -> None:
        patterns = patterns or DEFAULT_PATTERNS
        super().__init__(
            {fmt: re.compile(pattern) for fmt, pattern in patterns.items()}
        )

    def __str__(self) -> str:
        return "[DigitDate]"

    def prepare_sentence(self, sentence: str) -> str:
        return sentence.replace("\\", "/")

    def day(self, p: tuple) -> int:
        self._check_parts(p)
        return int(p[self._pattern_parts["day"]])

    def month(self, p: tuple) -> int:
        self._check_parts(p)
        return int(p[self._pattern_parts["month"]])

    def year(self, p) -> int:
        self._check_parts(p)
        return full_year(int(p[self._pattern_parts["year"]]))
