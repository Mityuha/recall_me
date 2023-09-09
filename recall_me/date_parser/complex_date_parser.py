from datetime import date
from typing import Final, Iterable

from loguru import logger

from .exceptions import AmbiguousParseResults
from .interfaces import DateParser


def next_notification(pdate: date) -> date:
    d = pdate.replace(year=date.today().year)
    if d > date.today():
        return d

    return d.replace(year=d.year + 1)


class ComplexDateParser:
    def __init__(self, *parsers: DateParser) -> None:
        self.parsers: Final[Iterable[DateParser]] = parsers

    def parse(self, text: str) -> dict[str, list[date]]:
        sentences: list[str] = text.split("\n")

        parser_results: dict[DateParser, dict[str, list[date]]] = {}

        for parser in self.parsers:
            tmp_results = ((sentence, parser.parse(sentence)) for sentence in sentences)
            parser_results[parser] = {
                sentence: result for sentence, result in tmp_results if result
            }
            logger.debug(f"Parser {parser} results: {parser_results[parser]}")

        parsers_processed: list[DateParser] = []

        sentence_2_dates: dict[str, list[date]] = {}

        for parser, results in parser_results.items():
            parsers_processed.append(parser)

            for a_parser, a_results in parser_results.items():
                if a_parser in parsers_processed:
                    continue

                for sentence, dates in results.items():
                    if sentence in a_results and set(dates) != set(a_results[sentence]):
                        year = date.today().year
                        dates1 = {d.replace(year=year) for d in dates}
                        dates2 = {d.replace(year=year) for d in a_results[sentence]}
                        if dates1 != dates2:
                            logger.error(
                                f"Parsers {parser} and {a_parser} "
                                "gave different results "
                                f"for the same sentence: '{sentence}'. "
                                f"'{parser}' results: {dates}. "
                                f"'{a_parser}' results: {a_results[sentence]}"
                            )
                            raise AmbiguousParseResults(
                                parser1=parser,
                                parser2=a_parser,
                                sentence=sentence,
                            )

            for sentence, dates in results.items():
                sentence_2_dates[sentence] = dates

        return {
            sentence: [next_notification(d) for d in dates]
            for sentence, dates in sentence_2_dates.items()
        }
