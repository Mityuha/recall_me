from typing import Any

from recall_me.calendar import SmartTitle


def test_smart_title(mocker: Any, faker: Any) -> None:
    stemmer: Any = mocker.Mock(stem=lambda w: w)
    max_words: int = faker.pyint(min_value=1, max_value=9)
    smart_title = SmartTitle(
        stemmer=stemmer,
        stop_words=[],
        max_words=max_words,
    )
    words: list[str] = [faker.pystr() for _ in range(10)]

    title = smart_title(" ".join(words))
    assert title == " ".join(words[:max_words])


def test_stop_words(mocker: Any, faker: Any) -> None:
    max_words: int = faker.pyint(min_value=1, max_value=9)
    stop_words: list[str] = [faker.pystr().lower() for _ in range(3)]
    smart_title = SmartTitle(
        stemmer=mocker.Mock(stem=lambda w: w),
        stop_words=stop_words,
        max_words=max_words,
    )

    correct_words = [faker.pystr()] * (max_words - 1)
    words = stop_words[:1] + correct_words + stop_words[1:]
    title = smart_title(" ".join(words))
    assert title == " ".join(correct_words)


def test_dates(mocker: Any, faker: Any) -> None:
    max_words: int = faker.pyint(min_value=1, max_value=9)
    smart_title = SmartTitle(
        stemmer=mocker.Mock(stem=lambda w: w), stop_words=[], max_words=max_words
    )

    word = faker.pystr()
    words = ["20.03.22", "2022-2-12", word, "2023/12/12"]
    title = smart_title(" ".join(words))
    assert title == word


def test_title_is_the_whole_text(mocker: Any, faker: Any) -> None:
    max_words: int = faker.pyint(min_value=1, max_value=9)
    stop_words = [faker.pystr().lower() for _ in range(10)]
    smart_title = SmartTitle(
        stemmer=mocker.Mock(stem=lambda w: w),
        stop_words=stop_words,
        max_words=max_words,
    )

    title = smart_title(" ".join(stop_words))
    assert title == " ".join(stop_words[:max_words])
