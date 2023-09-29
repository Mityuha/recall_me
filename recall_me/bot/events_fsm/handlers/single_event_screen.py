from typing import Callable, Final, Iterable

from recall_me.logging import logger
from telegram import CallbackQuery, InlineKeyboardMarkup

from ..types import AllEventsState
from .interfaces import EventInfo, EventsGetter


class SingleEventBack:
    def __init__(self, all_events_markup: Callable, events: EventsGetter) -> None:
        self.all_events_markup: Final[Callable] = all_events_markup
        self.events: Final[EventsGetter] = events

    def __str__(self) -> str:
        return "[SingleEventBack]"

    async def go_to_all_events(
        self,
        user_id: str,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        state: AllEventsState,
    ) -> AllEventsState:
        logger.debug(f"{self}: Getting all user '{user_id}' events.")

        events: Iterable[EventInfo] = await self.events.get_user_events(user_id)

        reply_markup: InlineKeyboardMarkup = self.all_events_markup(
            callback_id=callback_id,
            events=events,
        )

        await query.edit_message_text("Ваши события", reply_markup=reply_markup)
        return AllEventsState.CMD_ALL_EVENTS_SCREEN


# class AllEventsScreenChosen:
#     def __init__(self, events: EventInfoGetter) -> None:
#         self.events: Final[EventInfoGetter] = events

#     async def show_single_event(
#         self,
#         user_id: str,
#         callback_id: str,
#         callback_data: str,
#         query: CallbackQuery,
#         state: AllEventsState,
#     ) -> tuple[AllEventsState, Any]:
#         event_id: str = callback_data

#         event: EventInfo = await self.events.get_event_info(event_id)

#         buttons: list[list[InlineKeyboardButton]] = [
#             [
#                 InlineKeyboardButton(
#                     "Удалить", callback_data=f"{callback_id}-{DELETE_EVENT}"
#                 )
#             ],
#             [
#                 InlineKeyboardButton(
#                     "Назад", callback_data=f"{callback_id}-{BACK_ARROW}"
#                 )
#             ],
#         ]

#         text: str = f"""
#     <pre>
#     {event.title}
#     Дата        : {event.edate.strftime('%d.%m.%Y')}
#     Описание    : {event.description}
#     </pre>
#         """

#         await query.edit_message_text(
#             text,
#             reply_markup=InlineKeyboardMarkup(buttons),
#             parse_mode="HTML",
#         )
#         voice_message_id: int | None = None
#         if event.voice_id:
#             assert query.message
#             message: Message = query.message
#             msg: Message = await message.reply_voice(event.voice_id)
#             voice_message_id = msg.message_id

#         return (AllEventsState.SINGLE_EVENT_SCREEN, voice_message_id)
