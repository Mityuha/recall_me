from typing import Callable, Final, Iterable, TypedDict

from recall_me.logging import logger
from telegram import CallbackQuery, InlineKeyboardMarkup

from ..types import AllEventsState
from .interfaces import (CallbackMetadata, EventInfo, EventsDeleter,
                         EventsGetter)


class EventMetadata(TypedDict):
    voice_message_id: int | None
    event_id: int


class SingleEventBack:
    def __init__(self, all_events_markup: Callable, events: EventsGetter) -> None:
        self.all_events_markup: Final[Callable] = all_events_markup
        self.events: Final[EventsGetter] = events

    def __str__(self) -> str:
        return "[SingleEventBack]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        metadata: CallbackMetadata,
    ) -> AllEventsState:
        logger.debug(f"{self}: Getting all user '{metadata.user_id}' events.")

        events: Iterable[EventInfo] = await self.events.get_user_events(
            metadata.user_id
        )

        event_metadata: EventMetadata = metadata.metadata
        if event_metadata.get("voice_message_id"):
            await query.get_bot().delete_message(
                chat_id=int(metadata.user_id),
                message_id=event_metadata["voice_message_id"],
            )

        reply_markup: InlineKeyboardMarkup = self.all_events_markup(
            callback_id=callback_id,
            events=events,
        )

        await query.edit_message_text("Ваши события", reply_markup=reply_markup)
        return AllEventsState.CMD_ALL_EVENTS_SCREEN


class SingleEventDelete:
    def __init__(
        self,
        *,
        all_events_markup: Callable,
        events_getter: EventsGetter,
        events_deleter: EventsDeleter,
    ) -> None:
        self.all_events_markup: Final[Callable] = all_events_markup
        self.events_deleter: Final[EventsDeleter] = events_deleter
        self.events_getter: Final[EventsGetter] = events_getter

    def __str__(self) -> str:
        return "[SingleEventDelete]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        metadata: CallbackMetadata,
    ) -> AllEventsState:
        """Delete event and go back."""
        logger.debug(f"{self}: Getting all user '{metadata.user_id}' events.")

        event_metadata: EventMetadata = metadata.metadata
        if event_metadata.get("voice_message_id"):
            await query.get_bot().delete_message(
                chat_id=int(metadata.user_id),
                message_id=event_metadata["voice_message_id"],
            )

        event_id: int = event_metadata["event_id"]

        logger.debug(f"{self}: User '{metadata.user_id}': delete event {event_id}")
        await self.events_deleter.delete_event(event_id)
        await query.answer("Событие успешно удалено", show_alert=True)

        events: Iterable[EventInfo] = await self.events_getter.get_user_events(
            metadata.user_id
        )
        reply_markup: InlineKeyboardMarkup = self.all_events_markup(
            callback_id=callback_id,
            events=events,
        )

        await query.edit_message_text("Ваши события", reply_markup=reply_markup)
        return AllEventsState.CMD_ALL_EVENTS_SCREEN
