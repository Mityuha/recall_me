
from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    bot_token: str = Field(..., env="RECALL_ME_BOT_TOKEN")
    postgres_dsn: PostgresDsn = Field(
        "postgresql://recallme:recallme@127.0.0.1:5432/recallme"
    )
