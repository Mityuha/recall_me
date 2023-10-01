from typing import Any, Callable, Final

from telegram import CallbackQuery, InlineKeyboardMarkup

from ..types import AllEventsState
from .cron_utils import CronEvent, event_dict_to_object
from .interfaces import CallbackState


class CronConfigureClick:
    def __init__(self, events_reply_markup: Callable) -> None:
        self.events_reply_markup: Final[Callable] = events_reply_markup

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> tuple[AllEventsState, Any]:
        events: list[CronEvent] = callback_state.metadata

        events_objects: list = [event_dict_to_object(e) for e in events]

        reply_markup: InlineKeyboardMarkup = self.events_reply_markup(
            callback_id=callback_id,
            events=events_objects,
        )
        await query.edit_message_caption(
            "Ваши события",
            reply_markup=reply_markup,
        )

        return AllEventsState.CRON_ALL_EVENTS_SCREEN, events
