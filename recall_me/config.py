from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    bot_token: str = Field(..., env="RECALL_ME_BOT_TOKEN")
    text_model_path: Path = Path(".") / "vosk-model-small-ru-0.22.zip"
    title_max_words: int = 3
    postgres_dsn: PostgresDsn = Field(
        "postgresql://recallme:recallme@127.0.0.1:5432/recallme"
    )
