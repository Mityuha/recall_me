from telegram import Update
from telegram.ext import Application, MessageHandler, filters

from .bot import TextHandler, VoiceHandler
from .config import Settings


def main() -> None:
    # Create the Application and pass it your bot's token.
    settings = Settings()
    application = Application.builder().token(settings.bot_token).build()

    text_handler = TextHandler()
    voice_handler = VoiceHandler()

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, voice_handler)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
