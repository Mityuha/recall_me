import asyncio
import os
from datetime import date
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, run
from typing import Any, Final

from pydantic import BaseSettings, Field, PostgresDsn
from telegram import Bot


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        "postgresql://recallme:recallme@127.0.0.1:5432/recallme"
    )
    pg_dump: Path = Field("/usr/bin/pg_dump")
    backup_path: Path = Field("/home/bot/recall_me/backups")
    bot_token: str = Field(..., env="RECALL_ME_BOT_TOKEN")
    notify_chat_id: str = Field("5645779290")
    exclude_tables: list[str] = [
        "event_state",
        "screen_state",
        "event_state_id_seq",
        "screen_state_id_seq",
    ]
    backup_repo_path: Path = Field("/home/bot/recall_me_backup")
    git_path: Path = Field("/usr/bin/git")
    git_push_days: list[int] = [1, 15]


class ProcessNotify:
    def __init__(self, bot: Bot, chat_id: str) -> None:
        self.bot: Final[Bot] = bot
        self.chat_id: Final[str] = chat_id

    async def run_and_notify(self, cmds: list[str], **kwargs: Any) -> int:
        result: CompletedProcess | CalledProcessError
        try:
            result = run(cmds, check=True, **kwargs)
        except CalledProcessError as e:
            result = e
        except FileNotFoundError as e:
            result = CalledProcessError(
                returncode=2,
                cmd=" ".join(cmds),
                output=b"",
                stderr=f"FileNotFoundError: {str(e)}".encode(),
            )

        if result.returncode:
            stdout = result.stdout or b""
            stderr = result.stderr or b""
            text = "\n\n".join([stdout.decode(), stderr.decode()])
            text = f"[PGBackup]: {text}"

            async with self.bot:
                await self.bot.send_message(chat_id=self.chat_id, text=text)

        return result.returncode


async def main() -> None:
    config = Config()  # type: ignore
    bot = Bot(config.bot_token)

    config.backup_path.mkdir(exist_ok=True)

    today: date = date.today()
    backup_path: Path = config.backup_path / f"backup_{today.strftime('%d_%m_%Y')}.sql"

    exclude_tables: str = "-T " + " -T ".join(config.exclude_tables)

    process: ProcessNotify = ProcessNotify(bot=bot, chat_id=config.notify_chat_id)

    with backup_path.open("w") as bpath:
        await process.run_and_notify(
            [
                str(config.pg_dump),
                "--column-inserts",
                "--data-only",
                str(config.postgres_dsn),
                exclude_tables,
            ],
            stdout=bpath,
        )

    if today.day not in config.git_push_days:
        return

    assert config.backup_repo_path.exists()

    await process.run_and_notify(
        ["cp", str(backup_path), str(config.backup_repo_path)],
        capture_output=True,
    )

    os.chdir(config.backup_repo_path)

    for cmds in (
        [str(config.git_path), "add", str(backup_path.name)],
        ["git", "commit", "-m", f"'Database backup {backup_path.name}'"],
        ["git", "push"],
    ):
        returncode = await process.run_and_notify(
            cmds,
            capture_output=True,
        )

        if returncode:
            return

    await process.run_and_notify(
        ["rm", "-rf", str(config.backup_path)],
        capture_output=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
