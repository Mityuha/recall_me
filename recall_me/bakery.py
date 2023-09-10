from bakery import Bakery, Cake

from .bot import TextHandler, VoiceHandler
from .config import Settings
from .utils import Ogg2WavConverter, TextRecognizer, check_ffmpeg


class Container(Bakery):
    _ = Cake(check_ffmpeg)
    settings: Settings = Cake(Settings)  # type: ignore
    framerate: int = Cake(16000)

    text_recognizer: TextRecognizer = Cake(
        TextRecognizer,
        settings.text_model_path,
        framerate=framerate,
    )
    ogg_2_wav: Ogg2WavConverter = Cake(
        Ogg2WavConverter,
        framerate,
    )

    voice_handler: VoiceHandler = Cake(
        VoiceHandler,
        text_recognizer=text_recognizer,
        ogg_2_wav=ogg_2_wav,
    )

    text_handler: TextHandler = Cake(TextHandler)
