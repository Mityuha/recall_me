from recall_me.logging import logger
from telegram import Update
from telegram.ext import ContextTypes


class TextHandler:
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return "[TextHandler]"

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not update.message:
            return

        logger.debug(f"{self}: message received: {update.message}")
