from bakery import Bakery, Cake

from .bot import TextHandler, VoiceHandler
from .calendar import SmartTitle
from .config import Settings
from .date_parser import (ComplexDateParser, DateParser, DayMonthTextStrategy,
                          DigitDateStrategy, EventFormatter, MonthTextStrategy)
from .utils import Ogg2WavConverter, TextRecognizer, check_ffmpeg


class Container(Bakery):
    _ = Cake(check_ffmpeg)
    settings: Settings = Cake(Settings)  # type: ignore
    framerate: int = Cake(16000)

    text_recognizer: TextRecognizer = Cake(
        TextRecognizer,
        settings.text_model_path,
        framerate=framerate,
    )
    ogg_2_wav: Ogg2WavConverter = Cake(
        Ogg2WavConverter,
        framerate,
    )

    digit_date_strategy: DigitDateStrategy = Cake(DigitDateStrategy)
    month_text_strategy: MonthTextStrategy = Cake(MonthTextStrategy)
    day_month_text_strategy: DayMonthTextStrategy = Cake(DayMonthTextStrategy)

    date_parser: ComplexDateParser = Cake(
        ComplexDateParser,
        Cake(DateParser, digit_date_strategy),
        Cake(DateParser, month_text_strategy),
        Cake(DateParser, day_month_text_strategy),
    )

    title_maker: SmartTitle = Cake(
        SmartTitle,
        max_words=settings.title_max_words,
    )

    event_formatter: EventFormatter = Cake(EventFormatter, title_maker)

    voice_handler: VoiceHandler = Cake(
        VoiceHandler,
        text_recognizer=text_recognizer,
        ogg_2_wav=ogg_2_wav,
        date_parser=date_parser,
        event_formatter=event_formatter,
    )

    text_handler: TextHandler = Cake(TextHandler)
