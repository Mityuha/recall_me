import json
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import pyaudio
from recall_me.date_parser import MONTH_NUM_2_NAME, DayTextDateParser
from vosk import KaldiRecognizer, Model

model_name = Path("vosk-model-small-ru-0.22.zip")
zip_model = ZipFile(Path(__file__).parent / model_name)


with TemporaryDirectory() as tempdir:
    zip_model.extractall(tempdir)

    model = Model(str(Path(tempdir) / model_name.stem))

recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8192,
)
stream.start_stream()

parser = DayTextDateParser()

while True:
    try:
        data = stream.read(4096)
    except KeyboardInterrupt:
        break

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        result: dict = json.loads(text)
        if result.get("text"):
            dates: list[date] = parser.parse(result["text"])
            dates_text = [
                f"{d.day} {MONTH_NUM_2_NAME[d.month][0]} {d.year}" for d in dates
            ]
            print(result["text"], "==>", dates_text)
        # print(f"' {text[14:-3]} '")
