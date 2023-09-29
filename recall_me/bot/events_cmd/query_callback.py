from typing import Final
from uuid import uuid4

from telegram import InlineKeyboardMarkup, Message

from .funcs import events_reply_markup
from .interfaces import Event, StorageSave
from .types import AllEventsState


class CallbackHandler:
    def __init__(
        self,
        storage: StorageSave,
    ) -> None:
        self.storage: Final[StorageSave] = storage

    async def show_events(self, message: Message, events: list[Event]) -> None:
        if not message.from_user:
            return
        user_id: str = str(message.from_user.id)
        state: AllEventsState = AllEventsState.CMD_ALL_EVENTS_SCREEN
        callback_id: str = str(uuid4())
        reply_markup: InlineKeyboardMarkup = events_reply_markup(
            callback_id=callback_id,
            events=events,
        )
        chat_message: Message = await message.reply_text(
            "Ваши события",
            reply_markup=reply_markup,
        )
        await self.storage.save_state(
            callback_id=callback_id,
            user_id=user_id,
            message_id=chat_message.message_id,
            current_state=state,
        )

        # callback_id: str = ""
        # state: AllEventsState
        # state_data: Any
        # state, state_data = self.states[user_id]
        # query: CallbackQuery | None
        # voice_message: Message | None = None

        # if state == AllEventsState.ALL_EVENTS_SCREEN:
        #     query = state_data
        # elif state == AllEventsState.SINGLE_EVENT_SCREEN:
        #     _event_info: EventInfo
        #     _query: CallbackQuery
        #     _event_info, _query = state_data
        #     callback_id = await show_event(
        #         event=_event_info,
        #         query=_query,
        #     )
        #     voice_message = await send_voice(
        #         message=message,
        #         event=_event_info,
        #     )

        # self.channels[callback_id] = Queue()
        # data: str = ""
        # data, query = await self.wait_for_reply(callback_id)
        # if not data:
        #     logger.info(f"{self}: User '{user_id}' finished with state {state.name}")
        #     self.states.pop(user_id, None)
        #     break

        # assert query

        # if state == AllEventsState.ALL_EVENTS_SCREEN:
        #     if data == BACK_ARROW:
        #         logger.debug(f"{self}: User '{user_id}' closed events")
        #         await delete_message(query)
        #         break
        #     event_id: str = data
        #     event_info: EventInfo = await self.event_info_getter.get_event_info(
        #         event_id
        #     )
        #     self.states[user_id] = (
        #         AllEventsState.SINGLE_EVENT_SCREEN,
        #         (event_info, query),
        #     )

        # elif state == AllEventsState.SINGLE_EVENT_SCREEN:
        #     event, _query = state_data
        #     if data == BACK_ARROW:
        #         self.states[user_id] = (
        #             AllEventsState.ALL_EVENTS_SCREEN,
        #             query,
        #         )
        #     elif data == DELETE_EVENT:
        #         await self.event_deleter.delete_event(event.eid)
        #         await notify_event_delete(event=event, query=_query)
        #         self.states[user_id] = (
        #             AllEventsState.ALL_EVENTS_SCREEN,
        #             query,
        #         )
        #         events = [e for e in events if e.eid != event.eid]
        #     await delete_message_itself(voice_message)

    # async def wait_for_reply(
    # self, callback_id: str
    # ) -> tuple[str, CallbackQuery | None]:
    # channel: Queue = self.channels[callback_id]
    # data: str = ""
    # query: CallbackQuery
    # try:
    #     data, query = await wait_for(channel.get(), self.timeout)
    # except AioTimeoutError:
    #     logger.debug(f"{self}: User did nothing " f"for {self.timeout} seconds")
    # finally:
    #     self.channels.pop(callback_id)

    # if not data:
    #     return "", None

    # return data, query

    # def __str__(self) -> str:
    # return "[EventChosen]"
