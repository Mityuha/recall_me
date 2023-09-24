from asyncio import Queue
from asyncio import TimeoutError as AioTimeoutError
from asyncio import wait_for
from typing import Any, Final

from recall_me.logging import logger
from telegram import CallbackQuery, Message

from .funcs import (delete_message, delete_message_itself, notify_event_delete,
                    send_events, send_voice, show_event)
from .interfaces import Event, EventDeleter, EventInfo, EventInfoGetter
from .types import BACK_ARROW, DELETE_EVENT, AllEventsState


class CallbackHandler:
    def __init__(
        self,
        channels: dict[str, Queue],
        *,
        event_info_getter: EventInfoGetter,
        event_deleter: EventDeleter,
        timeout: int = 5 * 60,
    ) -> None:
        self.channels: Final[dict[str, Queue]] = channels
        self.event_info_getter: Final[EventInfoGetter] = event_info_getter
        self.event_deleter: Final[EventDeleter] = event_deleter
        self.timeout: Final[int] = timeout
        self.states: Final[dict[str, tuple[AllEventsState, Any]]] = {}

    async def show_events(self, message: Message, events: list[Event]) -> None:
        if not message.from_user:
            return
        user_id: str = str(message.from_user.id)
        self.states[user_id] = (AllEventsState.ALL_EVENTS_SCREEN, None)

        while True:
            callback_id: str = ""
            state: AllEventsState
            state_data: Any
            state, state_data = self.states[user_id]
            query: CallbackQuery | None
            voice_message: Message | None = None

            if state == AllEventsState.ALL_EVENTS_SCREEN:
                query = state_data
                callback_id = await send_events(
                    message,
                    events=events,
                    query=query,
                )
            elif state == AllEventsState.SINGLE_EVENT_SCREEN:
                _event_info: EventInfo
                _query: CallbackQuery
                _event_info, _query = state_data
                callback_id = await show_event(
                    event=_event_info,
                    query=_query,
                )
                voice_message = await send_voice(
                    message=message,
                    event=_event_info,
                )

            self.channels[callback_id] = Queue()
            data: str = ""
            data, query = await self.wait_for_reply(callback_id)
            if not data:
                logger.info(
                    f"{self}: User '{user_id}' finished with state {state.name}"
                )
                self.states.pop(user_id, None)
                break

            assert query

            if state == AllEventsState.ALL_EVENTS_SCREEN:
                if data == BACK_ARROW:
                    logger.debug(f"{self}: User '{user_id}' closed events")
                    await delete_message(query)
                    break
                event_id: str = data
                event_info: EventInfo = await self.event_info_getter.get_event_info(
                    event_id
                )
                self.states[user_id] = (
                    AllEventsState.SINGLE_EVENT_SCREEN,
                    (event_info, query),
                )

            elif state == AllEventsState.SINGLE_EVENT_SCREEN:
                event, _query = state_data
                if data == BACK_ARROW:
                    self.states[user_id] = (
                        AllEventsState.ALL_EVENTS_SCREEN,
                        query,
                    )
                elif data == DELETE_EVENT:
                    await self.event_deleter.delete_event(event.eid)
                    await notify_event_delete(event=event, query=_query)
                    self.states[user_id] = (
                        AllEventsState.ALL_EVENTS_SCREEN,
                        query,
                    )
                    events = [e for e in events if e.eid != event.eid]
                await delete_message_itself(voice_message)

    async def wait_for_reply(
        self, callback_id: str
    ) -> tuple[str, CallbackQuery | None]:
        channel: Queue = self.channels[callback_id]
        data: str = ""
        query: CallbackQuery
        try:
            data, query = await wait_for(channel.get(), self.timeout)
        except AioTimeoutError:
            logger.debug(f"{self}: User did nothing " f"for {self.timeout} seconds")
        finally:
            self.channels.pop(callback_id)

        if not data:
            return "", None

        return data, query

    def __str__(self) -> str:
        return "[EventChosen]"
