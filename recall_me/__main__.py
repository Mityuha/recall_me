import traceback
from asyncio import new_event_loop, set_event_loop

from telegram import Update
from telegram.error import TimedOut
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

import bakery

from .bakery import Container
from .logging import logger

bakery.logger = None


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")

    tb_list = traceback.format_exception(
        None,
        context.error,
        context.error.__traceback__,  # type: ignore
    )
    tb_string = "".join(tb_list)

    logger.error(tb_string)


def main() -> None:
    # Create the Application and pass it your bot's token.

    loop = new_event_loop()
    set_event_loop(loop)
    bakery: Container = loop.run_until_complete(Container.aopen())

    application = Application.builder().token(bakery.settings.bot_token).build()
    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bakery.text_handler)
    )
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, bakery.voice_handler)
    )

    application.add_handler(CallbackQueryHandler(bakery.callback_query_handler.handle))
    application.add_handler(CommandHandler("events", bakery.cmd_event_handler))

    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    try:
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            close_loop=False,
        )
    except TimedOut as exc:
        logger.warning(f"Telegram timed out: {exc}")
    finally:
        loop.run_until_complete(bakery.aclose())
        loop.close()


if __name__ == "__main__":
    main()
