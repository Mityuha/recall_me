from databases import Database
from recall_me.calendar import SmartCalendar
from recall_me.database import StateStorage, UserEvents
from telegram import Bot

from bakery import Bakery, Cake

from .config import Settings
from .database import BotUsers
from .notifier import Notifier


class Container(Bakery):
    settings: Settings = Cake(Settings)  # type: ignore
    bot: Bot = Cake(Cake(Bot, settings.bot_token))

    database: Database = Cake(Cake(Database, settings.postgres_dsn))
    bot_users: BotUsers = Cake(BotUsers, database)
    user_events: UserEvents = Cake(UserEvents, database)

    smart_calendar: SmartCalendar = Cake(SmartCalendar)
    state_storage: StateStorage = Cake(StateStorage, database)

    notifier: Notifier = Cake(
        Notifier,
        bot=bot,
        bot_users=bot_users,
        user_events=user_events,
        smart_calendar=smart_calendar,
        storage=state_storage,
    )
