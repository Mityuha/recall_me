from databases import Database
from recall_me.calendar import SmartCalendar
from recall_me.database import StateStorage
from recall_me.date_parser import HoursGrid
from telegram import Bot

from bakery import Bakery, Cake

from .config import Settings
from .database import BotUsers, UserRangeEvents
from .notifier import Notifier


class Container(Bakery):
    settings: Settings = Cake(Settings)  # type: ignore
    bot: Bot = Cake(Cake(Bot, settings.bot_token))

    database: Database = Cake(Cake(Database, settings.postgres_dsn))
    bot_users: BotUsers = Cake(BotUsers, database)
    user_events: UserRangeEvents = Cake(UserRangeEvents, database)

    smart_calendar: SmartCalendar = Cake(SmartCalendar)
    state_storage: StateStorage = Cake(StateStorage, database)

    hours_grid: HoursGrid = Cake(HoursGrid)

    notifier: Notifier = Cake(
        Notifier,
        bot=bot,
        bot_users=bot_users,
        user_events=user_events,
        smart_calendar=smart_calendar,
        storage=state_storage,
        hours_grid=hours_grid,
    )
