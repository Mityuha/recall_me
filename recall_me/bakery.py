from typing import Any

from databases import Database

from bakery import Bakery, Cake

from .bot import (CallbackQueryHandler, Event2Text, EventsCommand, Handler,
                  TextEvents, VoiceEvents)
from .bot.events_fsm import (AllEventsScreenBack, AllEventsScreenChosen,
                             CallbackRouter, IStateHandler, SaveEventsNo,
                             SaveEventsYes, SingleEventBack, SingleEventDelete)
from .bot.types import BACK_ARROW, DELETE_EVENT, NO, YES, AllEventsState
from .bot.utils import events_reply_markup
from .calendar import SmartTitle
from .config import Settings
from .database import (DeleteEvent, EventInfo, SaveEvent, StateStorage,
                       UserEvents)
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
    state_storage: StateStorage = Cake(StateStorage)
    text_handler: Handler = Cake(
        Handler,
        text_events,
        storage=state_storage,
        description="TextHandler",
        event_formatter=event_2_text,
    )
    voice_handler: Handler = Cake(
        Handler,
        voice_events,
        storage=state_storage,
        description="VoiceHandler",
        event_formatter=event_2_text,
    )

    database: Database = Cake(Cake(Database, settings.postgres_dsn))
    event_saver: SaveEvent = Cake(SaveEvent, database)

    event_info_getter: EventInfo = Cake(EventInfo, database)
    event_deleter: DeleteEvent = Cake(DeleteEvent, database)
    user_events_getter: UserEvents = Cake(UserEvents, database)

    state_handlers: dict[Any, IStateHandler] = Cake(
        {
            (AllEventsState.CMD_ALL_EVENTS_SCREEN, BACK_ARROW): Cake(
                AllEventsScreenBack
            ),
            AllEventsState.CMD_ALL_EVENTS_SCREEN: Cake(
                AllEventsScreenChosen, event_info_getter
            ),
            (AllEventsState.CMD_SINGLE_EVENT_SCREEN, BACK_ARROW): Cake(
                SingleEventBack,
                all_events_markup=events_reply_markup,
                events=user_events_getter,
            ),
            (AllEventsState.CMD_SINGLE_EVENT_SCREEN, DELETE_EVENT): Cake(
                SingleEventDelete,
                all_events_markup=events_reply_markup,
                events_getter=user_events_getter,
                events_deleter=event_deleter,
            ),
            (AllEventsState.SAVE_EVENTS_SCREEN, YES): Cake(SaveEventsYes, event_saver),
            (AllEventsState.SAVE_EVENTS_SCREEN, NO): Cake(SaveEventsNo),
        }
    )

    callback_router: CallbackRouter = Cake(
        CallbackRouter,
        storage=state_storage,
        handlers=state_handlers,
    )

    callback_query_handler: CallbackQueryHandler = Cake(
        CallbackQueryHandler,
        storage=state_storage,
        router=callback_router,
    )

    cmd_event_handler: EventsCommand = Cake(
        EventsCommand,
        storage=state_storage,
        events_getter=user_events_getter,
        events_reply_markup=events_reply_markup,
    )
