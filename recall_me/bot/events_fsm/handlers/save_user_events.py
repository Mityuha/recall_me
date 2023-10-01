from asyncio import gather
from datetime import date
from typing import Final, TypedDict

from recall_me.logging import logger
from telegram import CallbackQuery

from ..types import AllEventsState
from .interfaces import CallbackState, EventSaver


class Event(TypedDict):
    title: str
    description: str
    edate: str
    start_hour: int
    duration: int


class EventMetadata(TypedDict):
    voice_file_id: str | None
    message_text: str
    events: list[Event]


class SaveEventsYes:
    def __init__(self, event_saver: EventSaver) -> None:
        self.event_saver: Final[EventSaver] = event_saver

    def __str__(self) -> str:
        return "[SaveEventYes]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> AllEventsState:
        logger.info(
            f"{self}: User '{callback_state.user_id}' "
            "confirmed events saving. Save events."
        )

        event_metadata: EventMetadata = callback_state.metadata

        try:
            await gather(
                *[
                    self.event_saver.save_event(
                        title=e["title"],
                        description=e["description"],
                        event_day=date.fromisoformat(e["edate"]).day,
                        event_month=date.fromisoformat(e["edate"]).month,
                        voice_id=event_metadata["voice_file_id"],
                        source_text=event_metadata["message_text"],
                        author_id=callback_state.user_id,
                        duration=e["duration"],
                        start_hour=e["start_hour"],
                    )
                    for e in event_metadata["events"]
                ]
            )
        except Exception as exc:
            logger.error(
                f"{self}: exception occured while saving events: {exc}; "
                f"events = {event_metadata['events']}"
            )
            await query.edit_message_text(
                "При сохранении возникла ошибка. Попробуйте:\n"
                "0. повторить;\n"
                "1. eсли сообщение длинное -- сократить"
            )
        else:
            await query.edit_message_text("Успешно сохранено.")

        return AllEventsState.NO_MESSAGE


class SaveEventsNo:
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return "[SaveEventNo]"

    async def __call__(
        self,
        *,
        callback_id: str,
        callback_data: str,
        query: CallbackQuery,
        callback_state: CallbackState,
    ) -> AllEventsState:
        logger.info(f"{self}: User '{callback_state.user_id}' declined events saving.")
        await query.edit_message_text(text="Хорошо. Попробуйте еще раз.")
        return AllEventsState.NO_MESSAGE
