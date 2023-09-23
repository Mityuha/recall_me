from asyncio import new_event_loop

from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, MessageHandler,
                          filters)

from .bakery import Container


def main() -> None:
    # Create the Application and pass it your bot's token.

    loop = new_event_loop()
    bakery: Container = loop.run_until_complete(Container.aopen())

    application = Application.builder().token(bakery.settings.bot_token).build()
    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bakery.text_handler)
    )
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, bakery.voice_handler)
    )

    application.add_handler(CallbackQueryHandler(bakery.callback_query.handle))

    # Run the bot until the user presses Ctrl-C
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        loop.run_until_complete(bakery.aclose())


if __name__ == "__main__":
    main()
