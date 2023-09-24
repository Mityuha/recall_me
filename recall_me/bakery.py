from asyncio import Queue

from psycopg import AsyncConnection
from psycopg.rows import tuple_row

from bakery import Bakery, Cake

from .bot import (CallbackQuery, Event2Text, EventsConfirmation, Handler,
                  TextEvents, VoiceEvents)
from .bot.events_cmd import CallbackHandler, EventsCommand
from .calendar import SmartTitle
from .config import Settings
from .database import Database, DeleteEvent, EventInfo, SaveEvent, UserEvents
from .date_parser import (DAY_NAME_2_NUM, MONTH_NAME_2_NUM, ComplexDateParser,
                          DateParser, DayMonthTextStrategy, DigitDateStrategy,
                          EventFormatter, MonthTextStrategy)
from .utils import Ogg2WavConverter, TextRecognizer, check_ffmpeg

# from databases import Database


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

    # database: Database = Cake(Cake(Database, settings.postgres_dsn))
    connection: AsyncConnection = Cake(
        Cake(
            AsyncConnection.connect,
            settings.postgres_dsn,
            row_factory=tuple_row,  # type: ignore
            autocommit=True,
        )
    )
    database: Database = Cake(Database, connection)
    event_saver: SaveEvent = Cake(SaveEvent, database)

    text_handler: Handler = Cake(
        Handler,
        text_events,
        events_confirmation=events_confirmation,
        event_saver=event_saver,
        description="TextHandler",
    )
    voice_handler: Handler = Cake(
        Handler,
        voice_events,
        events_confirmation=events_confirmation,
        event_saver=event_saver,
        description="VoiceHandler",
    )

    event_info_getter: EventInfo = Cake(EventInfo, database)
    event_deleter: DeleteEvent = Cake(DeleteEvent, database)
    user_events_getter: UserEvents = Cake(UserEvents, database)

    events_screen: CallbackHandler = Cake(
        CallbackHandler,
        channels=channels,
        event_info_getter=event_info_getter,
        event_deleter=event_deleter,
    )

    cmd_event_handler: EventsCommand = Cake(
        EventsCommand,
        channels,
        events_getter=user_events_getter,
        events_screen=events_screen,
    )
