import re
from typing import Any, Final, Sequence

from nltk.stem.snowball import RussianStemmer  # type: ignore


class SmartTitle:
    def __init__(
        self,
        *,
        stemmer: Any = RussianStemmer(),
        stop_words: Sequence[str] = tuple(),
        max_words: int = 3,
    ) -> None:
        self.stemmer: Final[Any] = stemmer
        self.max_words: Final[int] = max_words
        self.stop_words: Final[Sequence[str]] = stop_words

    def __call__(self, title: str) -> str:
        words: list[str] = title.split()
        title_words: list[str] = []

        matcher: re.Pattern = re.compile(r"[a-zа-я]")
        for orig_word in words:
            if len(title_words) >= self.max_words:
                break

            word = orig_word.lower()
            if not matcher.match(word):
                continue

            stem_word = self.stemmer.stem(word)
            if stem_word in self.stop_words:
                continue

            title_words.append(orig_word)

        title_words = title_words or words[: self.max_words]
        return " ".join(title_words)
