from asyncio import Queue
from typing import Final

from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes


class CallbackQuery:
    def __init__(self, channels: dict[str, Queue]) -> None:
        self.channels: Final[dict[str, Queue]] = channels

    def __str__(self) -> str:
        return "[CallbackQuery]"

    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.callback_query:
            logger.info(f"{self}: update received, but no callback_query found")
            return

        query = update.callback_query
        await query.answer()
        if not query.data:
            logger.info(f"{self}: no callback query data found.")
            await query.delete_message()
            return

        logger.debug(
            f"{self}: Query answer received: '{query.data}' "
            f"from user {query.from_user.username}"
        )

        callback_id, callback_data = query.data.rsplit("-", 1)
        if callback_id not in self.channels:
            await query.edit_message_text(
                text="Похоже, что сообщение старое. Попробуйте еще раз"
            )
            return

        await self.channels[callback_id].put((callback_data, query))
