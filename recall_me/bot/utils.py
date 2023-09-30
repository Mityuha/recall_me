from typing import Iterable

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .interfaces import EventInfo as Event
from .types import BACK_ARROW


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
