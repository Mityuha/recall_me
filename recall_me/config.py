from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="RECALL_ME_BOT_TOKEN")
    text_model_path: Path = Path(".") / "vosk-model-small-ru-0.22.zip"
    title_max_words: int = 3
