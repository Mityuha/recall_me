import re
from typing import Final, Iterable

from loguru import logger


class PatternsMixin:
    def __init__(self, patterns: dict[str, re.Pattern]) -> None:
        self._patterns: Final[dict[str, re.Pattern]] = patterns
        self._pattern_parts: dict[str, int] = {}

    def patterns(self) -> Iterable[re.Pattern]:
        p_format: str
        pattern: re.Pattern
        for p_format, pattern in self._patterns.items():
            self._pattern_parts = {
                part: index for index, part in enumerate(p_format.split(" "))
            }
            logger.debug(f"{self}: check against pattern {p_format}")
            yield pattern

        self._pattern_parts = {}

    def _check_parts(self, parts: tuple) -> None:
        assert len(parts) == len(self._pattern_parts), (parts, self._pattern_parts)
