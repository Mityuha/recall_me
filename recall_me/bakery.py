from asyncio import Queue

from bakery import Bakery, Cake

from .bot import (CallbackQuery, Event2Text, EventsConfirmation, Handler,
                  TextEvents, VoiceEvents)
from .calendar import SmartTitle
from .config import Settings
from .date_parser import (DAY_NAME_2_NUM, MONTH_NAME_2_NUM, ComplexDateParser,
                          DateParser, DayMonthTextStrategy, DigitDateStrategy,
                          EventFormatter, MonthTextStrategy)
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
        stop_words=tuple(DAY_NAME_2_NUM) + tuple(MONTH_NAME_2_NUM) + ("двадца",),
        max_words=settings.title_max_words,
    )

    event_formatter: EventFormatter = Cake(EventFormatter, title_maker)

    voice_events: VoiceEvents = Cake(
        VoiceEvents,
        text_recognizer=text_recognizer,
        ogg_2_wav=ogg_2_wav,
        date_parser=date_parser,
        event_formatter=event_formatter,
    )

    text_events: TextEvents = Cake(
        TextEvents,
        date_parser=date_parser,
        event_formatter=event_formatter,
    )
    event_2_text: Event2Text = Cake(Event2Text)
    channels: dict[str, Queue] = Cake({})
    events_confirmation: EventsConfirmation = Cake(
        EventsConfirmation,
        channels=channels,
        event_formatter=event_2_text,
    )

    callback_query: CallbackQuery = Cake(CallbackQuery, channels)

    text_handler: Handler = Cake(
        Handler,
        text_events,
        events_confirmation=events_confirmation,
        description="TextHandler",
    )
    voice_handler: Handler = Cake(
        Handler,
        voice_events,
        events_confirmation=events_confirmation,
        description="VoiceHandler",
    )
