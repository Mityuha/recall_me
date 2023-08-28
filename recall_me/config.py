from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="RECALL_ME_BOT_TOKEN")
