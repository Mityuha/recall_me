from asyncio import create_task, gather, sleep
from typing import Final, Sequence

from recall_me.logging import logger
from telegram import Message, Update
from telegram.ext import ContextTypes

from .interfaces import (Event, EventSaver, EventsConfirmation, EventsGetter,
                         TextEditor)


class Handler:
    def __init__(
        self,
        events_getter: EventsGetter,
        *,
        events_confirmation: EventsConfirmation,
        event_saver: EventSaver,
        description: str = "Handler",
    ) -> None:
        self.event_getter: Final[EventsGetter] = events_getter
        self.events_confirmation: Final[EventsConfirmation] = events_confirmation
        self.event_saver: Final[EventSaver] = event_saver
        self._description: Final[str] = description

    def __str__(self) -> str:
        return f"[{self._description}]"

    async def process_in_background(
        self,
        *,
        message: Message,
        events: Sequence[Event],
    ) -> None:
        if not message.from_user:
            logger.error(f"Message {message} has got an empty attribute 'from_user'")
            return
        is_confirmed: bool
        text_editor: TextEditor

        is_confirmed, text_editor = await self.events_confirmation.send_confirmation(
            events,
            message=message,
        )

        if not is_confirmed:
            logger.info(f"{self}: User {message.chat.username} declined events saving.")
            await text_editor.edit_message_text(text="Хорошо. Попробуйте еще раз.")
            return

        logger.info(
            f"{self}: User {message.chat.username} "
            "confirmed events saving. Save events."
        )

        try:
            await gather(
                *[
                    self.event_saver.save_event(
                        title=e.title,
                        description=e.description,
                        event_day=e.edate.day,
                        event_month=e.edate.month,
                        voice_id=message.voice.file_id if message.voice else None,
                        source_text=message.text,
                        author_id=str(message.from_user.id),
                        duration=e.duration,
                        start_hour=e.start_hour,
                    )
                    for e in events
                ]
            )
        except Exception as exc:
            logger.error(
                f"{self}: exception occured while saving events: {exc}; {events = }"
            )
            await text_editor.edit_message_text(
                "При сохранении возникла ошибка. Попробуйте:\n"
                "0. повторить;\n"
                "1. eсли сообщение длинное -- сократить"
            )
        else:
            await text_editor.edit_message_text("Успешно сохранено.")

    async def __call__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        if not update.message:
            return

        events: Sequence[Event] = await self.event_getter(
            update=update,
            context=context,
        )

        create_task(
            self.process_in_background(
                message=update.message,
                events=events,
            )
        )
        await sleep(0)
