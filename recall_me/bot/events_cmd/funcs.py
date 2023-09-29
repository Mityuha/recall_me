from typing import Iterable
from uuid import uuid4

from telegram import (CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message)

from .interfaces import Event, EventInfo
from .types import BACK_ARROW, DELETE_EVENT


def events_reply_markup(
    *,
    callback_id: str,
    events: Iterable[Event],
) -> InlineKeyboardMarkup:
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            f"{e.edate.strftime('%d.%m')}  {e.title}",
            callback_data=f"{callback_id}-{e.eid}",
        )
        for e in events
    ]

    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append(
        [
            InlineKeyboardButton(
                "Закрыть",
                callback_data=f"{callback_id}-{BACK_ARROW}",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


async def send_events(
    message: Message,
    *,
    events: list[Event],
    query: CallbackQuery | None,
) -> str:
    str(uuid4())

    text: str = "Ваши события"
    new_message: Message
    if not query:
        new_message = await message.reply_text(text, reply_markup=reply_markup)
    else:
        new_message = await query.edit_message_text(text, reply_markup=reply_markup)
    return new_message.message_id


async def show_event(query: CallbackQuery, event: EventInfo) -> str:
    callback_id: str = str(uuid4())

    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                "Удалить", callback_data=f"{callback_id}-{DELETE_EVENT}"
            )
        ],
        [InlineKeyboardButton("Назад", callback_data=f"{callback_id}-{BACK_ARROW}")],
    ]

    text: str = f"""
<pre>
{event.title}
Дата        : {event.edate.strftime('%d.%m.%Y')}
Описание    : {event.description}
</pre>
    """

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML",
    )

    return callback_id


async def send_voice(message: Message, event: EventInfo) -> Message | None:
    if event.voice_id:
        msg: Message = await message.reply_voice(event.voice_id)
        return msg

    return None


async def notify_event_delete(event: EventInfo, query: CallbackQuery) -> None:
    await query.answer(f"Событие {event.title} успешно удалено", show_alert=True)


async def delete_message_itself(message: Message | None) -> None:
    if message:
        try:
            await message.delete()
        except Exception:
            pass


async def delete_message(query: CallbackQuery) -> None:
    await query.delete_message()
