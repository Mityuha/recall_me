from typing import Any, Callable, Final, TypedDict

from recall_me.logging import logger
from telegram import CallbackQuery, InlineKeyboardMarkup

from ..types import AllEventsState
from .cron_utils import CronEvent, event_dict_to_object
from .interfaces import CallbackState, EventsDeleter


class CronEventMetadata(TypedDict):
    events: list[CronEvent]
    voice_message_id: int | None
    event_id: int


class CronSingleEventBack:
    def __init__(self, events_reply_markup: Callable) -> None:
        self.events_reply_markup: Final[Callable] = events_reply_markup

    def __str__(self) -> str:
        return "[CronSingleEventBack]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> tuple[AllEventsState, Any]:
        logger.debug(f"{self}: Getting all user '{callback_state.user_id}' events.")

        metadata: CronEventMetadata = callback_state.metadata
        events = metadata["events"]

        events_objects: list = [event_dict_to_object(e) for e in events]

        reply_markup: InlineKeyboardMarkup = self.events_reply_markup(
            callback_id=callback_id,
            events=events_objects,
        )

        if metadata.get("voice_message_id"):
            await query.get_bot().delete_message(
                chat_id=int(callback_state.user_id),
                message_id=metadata["voice_message_id"],
            )
        await query.edit_message_caption(
            "Ваши события",
            reply_markup=reply_markup,
        )

        return AllEventsState.CRON_ALL_EVENTS_SCREEN, events


class CronSingleEventDelete:
    def __init__(
        self,
        *,
        events_reply_markup: Callable,
        events_deleter: EventsDeleter,
    ) -> None:
        self.events_reply_markup: Final[Callable] = events_reply_markup
        self.events_deleter: Final[EventsDeleter] = events_deleter

    def __str__(self) -> str:
        return "[CronSingleEventDelete]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> tuple[AllEventsState, Any]:
        """Delete event and go back."""
        logger.debug(f"{self}: Getting all user '{callback_state.user_id}' events.")

        metadata: CronEventMetadata = callback_state.metadata
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

        events: list[CronEvent] = [
            e for e in metadata["events"] if e["eid"] != event_id
        ]
        events_objects: list = [event_dict_to_object(e) for e in events]

        reply_markup: InlineKeyboardMarkup = self.events_reply_markup(
            callback_id=callback_id,
            events=events_objects,
        )

        await query.edit_message_caption("Ваши события", reply_markup=reply_markup)
        return (AllEventsState.CRON_ALL_EVENTS_SCREEN, events)
