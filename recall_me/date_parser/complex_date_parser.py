from datetime import date
from typing import Final, Iterable

from loguru import logger

from .interfaces import DateParser


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
                        assert False  # <<<<

            for sentence, dates in results.items():
                sentence_2_dates[sentence] = dates

        return sentence_2_dates
