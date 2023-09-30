from typing import Callable, Final, Iterable, TypedDict

from recall_me.logging import logger
from telegram import CallbackQuery, InlineKeyboardMarkup

from ..types import AllEventsState
from .interfaces import CallbackState, EventInfo, EventsDeleter, EventsGetter


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
        callback_state: CallbackState,
    ) -> AllEventsState:
        logger.debug(f"{self}: Getting all user '{callback_state.user_id}' events.")

        events: Iterable[EventInfo] = await self.events.get_user_events(
            callback_state.user_id
        )

        metadata: EventMetadata = callback_state.metadata
        if metadata.get("voice_message_id"):
            await query.get_bot().delete_message(
                chat_id=int(callback_state.user_id),
                message_id=metadata["voice_message_id"],
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
        callback_state: CallbackState,
    ) -> AllEventsState:
        """Delete event and go back."""
        logger.debug(f"{self}: Getting all user '{callback_state.user_id}' events.")

        metadata: EventMetadata = callback_state.metadata
        if metadata.get("voice_message_id"):
            await query.get_bot().delete_message(
                chat_id=int(callback_state.user_id),
                message_id=metadata["voice_message_id"],
            )

        event_id: int = metadata["event_id"]

        logger.debug(
            f"{self}: User '{callback_state.user_id}': delete event {event_id}"
        )
        await self.events_deleter.delete_event(event_id)
        await query.answer("Событие успешно удалено", show_alert=True)

        events: Iterable[EventInfo] = await self.events_getter.get_user_events(
            callback_state.user_id
        )
        reply_markup: InlineKeyboardMarkup = self.all_events_markup(
            callback_id=callback_id,
            events=events,
        )

        await query.edit_message_text("Ваши события", reply_markup=reply_markup)
        return AllEventsState.CMD_ALL_EVENTS_SCREEN
