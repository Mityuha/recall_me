from typing import Any, Final

from recall_me.logging import logger
from telegram import (CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message)

from ..types import BACK_ARROW, DELETE_EVENT, AllEventsState
from .interfaces import CallbackState, EventInfo, EventInfoGetter


class AllEventsScreenBack:
    @staticmethod
    async def __call__(
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> AllEventsState:
        logger.debug(f"EventsScreenBack: User '{callback_state.user_id}' closed events")

        await query.delete_message()
        return AllEventsState.NO_MESSAGE


class AllEventsScreenChosen:
    def __init__(self, events: EventInfoGetter) -> None:
        self.events: Final[EventInfoGetter] = events

    def __str__(self) -> str:
        return "[AllEventsScreenChosen]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> tuple[AllEventsState, Any]:
        event_id: str = callback_data

        event: EventInfo | None = await self.events.get_event_info(event_id)
        if not event:
            logger.debug(f"{self}: It seems that event {event_id} was deleted.")
            return (AllEventsState.CMD_ALL_EVENTS_SCREEN, None)

        buttons: list[list[InlineKeyboardButton]] = [
            [
                InlineKeyboardButton(
                    "Удалить", callback_data=f"{callback_id}-{DELETE_EVENT}"
                )
            ],
            [
                InlineKeyboardButton(
                    "Назад", callback_data=f"{callback_id}-{BACK_ARROW}"
                )
            ],
        ]

        text: str = f"""<pre>{event.title}
Дата        : {event.edate.strftime('%d.%m.%Y')}
Описание    : {event.description}
</pre>
        """

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML",
        )
        voice_message_id: int | None = None
        if event.voice_id:
            assert query.message
            message: Message = query.message
            msg: Message = await message.reply_voice(event.voice_id)
            voice_message_id = msg.message_id

        return (
            AllEventsState.CMD_SINGLE_EVENT_SCREEN,
            {
                "voice_message_id": voice_message_id,
                "event_id": event.eid,
            },
        )
