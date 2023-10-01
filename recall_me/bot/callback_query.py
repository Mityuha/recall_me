from asyncio import create_task, sleep
from typing import Any, Final

from recall_me.logging import logger
from telegram import CallbackQuery, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from .interfaces import Router, Storage


class CallbackQueryHandler:
    def __init__(self, storage: Storage, router: Router) -> None:
        self.storage: Final[Storage] = storage
        self.router: Final[Router] = router

    def __str__(self) -> str:
        return "[CallbackQuery]"

    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.callback_query:
            logger.info(f"{self}: update received, but no callback_query found")
            return

        query: CallbackQuery = update.callback_query
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
        callback_state: Any | None = await self.storage.callback_state(callback_id)

        if not callback_state:
            logger.warning(
                f"{self}: User {query.from_user.id}: "
                f"no callback state for {callback_id = }"
            )
            try:
                await query.edit_message_text(
                    text="Возможно, что сообщение старое. Попробуйте еще раз"
                )
            except BadRequest:
                await query.answer("Сообщение устарело", show_alert=True)

            async def sleep_and_delete(query: CallbackQuery) -> None:
                await sleep(1.5)
                await query.delete_message()

            await create_task(sleep_and_delete(query))
            return

        await create_task(
            self.router.route_callback(
                callback_id=callback_id,
                callback_data=callback_data,
                query=query,
                callback_state=callback_state,
            )
        )
