from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from zipfile import ZipFile

from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from vosk import KaldiRecognizer, Model

from .bot import TextHandler, VoiceHandler
from .config import Settings
from .utils import Ogg2WavConverter


def create_recognizer() -> Any:
    model_name = (
        Path("..") / "recall_me_tester" / "voice" / "vosk-model-small-ru-0.22.zip"
    )
    zip_model = ZipFile(Path(__file__).parent / model_name)

    with TemporaryDirectory() as tempdir:
        zip_model.extractall(tempdir)

        model = Model(str(Path(tempdir) / model_name.stem))

    recognizer = KaldiRecognizer(model, 16000)

    return recognizer


def main() -> None:
    # Create the Application and pass it your bot's token.
    settings = Settings()
    application = Application.builder().token(settings.bot_token).build()

    text_handler = TextHandler()

    recognizer = create_recognizer()
    ogg_2_wav = Ogg2WavConverter()
    voice_handler = VoiceHandler(recognizer, ogg_2_wav=ogg_2_wav)

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
