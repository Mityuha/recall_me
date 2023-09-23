from typing import Final

from .interfaces import DatabaseVal


class SaveEvent:
    def __init__(self, database: DatabaseVal) -> None:
        self.database: Final[DatabaseVal] = database

    async def save_event(
        self,
        *,
        title: str,
        description: str,
        event_day: int,
        event_month: int,
        voice_id: str | None,
        source_text: str | None,
        author_id: str,
        duration: int = 2,
        start_hour: int = -1,
        notify_before_days: int = 7,
    ) -> None:
        event_id: int = await self.database.fetch_val(
            "INSERT INTO event( "
            "title, description, event_day, "
            "event_month, voice_id, source_text, author_id) "
            "VALUES (:title, :description, :event_day, :event_month, "
            ":voice_id, :source_text, :author_id) "
            "RETURNING id;",
            {
                "title": title,
                "description": description,
                "event_day": event_day,
                "event_month": event_month,
                "voice_id": voice_id,
                "source_text": source_text,
                "author_id": author_id,
            },
        )

        await self.database.fetch_val(
            "INSERT INTO event_config("
            "event_id, duration, start_hour, notify_before_days) "
            "VALUES (:event_id, :duration, :start_hour, :notify_before_days) "
            "RETURNING id;",
            {
                "event_id": event_id,
                "duration": duration,
                "start_hour": start_hour,
                "notify_before_days": notify_before_days,
            },
        )
