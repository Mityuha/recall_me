from asyncio import gather
from collections import defaultdict
from datetime import date, timedelta
from io import BytesIO
from itertools import chain
from typing import Final, Iterable
from uuid import uuid4

from recall_me.bot.types import AllEventsState
from recall_me.logging import logger
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from .interfaces import (BotUsers, EventInfo, HoursGrid, SmartCalendar,
                         StorageSave, UserEvents)
from .types import BLANCHED_ALMOLD, IVORY, TEA_GREEN, TRANSPARENT
from .types import Event as CalendarEvent
from .types import EventStyle


def choose_style(edate: date) -> EventStyle:
    today = date.today()
    if edate < today:
        return IVORY
    if edate > today:
        return BLANCHED_ALMOLD

    return TEA_GREEN


class Notifier:
    def __init__(
        self,
        bot: Bot,
        *,
        bot_users: BotUsers,
        user_events: UserEvents,
        smart_calendar: SmartCalendar,
        storage: StorageSave,
        hours_grid: HoursGrid,
    ) -> None:
        self.bot: Final[Bot] = bot
        self.bot_users: Final[BotUsers] = bot_users
        self.user_events: Final[UserEvents] = user_events
        self.smart_calendar: Final[SmartCalendar] = smart_calendar
        self.storage: Final[StorageSave] = storage
        self.hours_grid: Final[HoursGrid] = hours_grid

    def __str__(self) -> str:
        return "[CronNotifier]"

    async def notify_user(self, user_id: str) -> None:
        today: date = date.today()
        from_date: date = today - timedelta(days=3)
        to_date: date = today + timedelta(days=3)
        events: Iterable[EventInfo] = await self.user_events.get_user_events(
            user_id,
            from_date=from_date,
            to_date=to_date,
        )

        if not any(
            e.edate in (from_date, from_date + timedelta(days=3)) for e in events
        ):
            logger.info(
                f"{self}: User {user_id} has no today's or 3 days before events."
            )
            return

        logger.debug(f"{self}: User {user_id} events: {events}")

        calendar_events: defaultdict[date, list[CalendarEvent]] = defaultdict(list)

        for e in events:
            calendar_events[e.edate].append(
                CalendarEvent(
                    edate=e.edate,
                    description=e.description,
                    title=e.title,
                    start_hour=e.start_hour,
                    duration=e.duration,
                    style=choose_style(e.edate),
                )
            )

        for event_list in calendar_events.values():
            for event, hour in zip(
                event_list, self.hours_grid.sort_events(len(event_list))
            ):
                event.start_hour = hour

        for i in range(-3, 4, 1):
            day = today + timedelta(days=i)
            if day in calendar_events:
                continue

            calendar_events[day] = [
                CalendarEvent(
                    edate=day,
                    style=TRANSPARENT,
                )
            ]

        calendar: bytes = self.smart_calendar.render(
            chain.from_iterable(calendar_events.values())
        )

        callback_id: str = str(uuid4())

        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Настроить", callback_data=f"{callback_id}-cfg")]]
        )

        await self.bot.send_photo(
            chat_id=user_id,
            photo=BytesIO(calendar),
            reply_markup=reply_markup,
        )

        logger.debug(f"{self}: User {user_id} successfully notified")

        metadata_events: list[dict] = [
            {
                "eid": e.eid,
                "title": e.title,
                "description": e.description,
                "edate": e.edate.isoformat(),
                "start_hour": e.start_hour,
                "duration": e.duration,
                "voice_id": e.voice_id,
            }
            for e in events
        ]

        await self.storage.save_state(
            callback_id=callback_id,
            user_id=user_id,
            previous_state=AllEventsState.NO_MESSAGE,
            current_state=AllEventsState.CRON_NOTIFY_MESSAGE_SCREEN,
            metadata=metadata_events,
        )

        logger.debug(f"{self}: User {user_id} state saved")

    async def notify_all(self) -> None:
        users: Iterable[str] = await self.bot_users.get_bot_users()

        logger.debug(f"{self}: Notify users: {users}")

        await gather(*[self.notify_user(user_id) for user_id in users])
