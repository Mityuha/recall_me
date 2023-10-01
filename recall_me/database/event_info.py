from datetime import date
from typing import Final

from .interfaces import DatabaseOne
from .types import Event


class EventInfo:
    def __init__(self, database: DatabaseOne) -> None:
        self.database: Final[DatabaseOne] = database

    async def get_event_info(
        self,
        event_id: str | int,
    ) -> Event | None:
        row = await self.database.fetch_one(
            "SELECT id, title, description, event_day, event_month, voice_id "
            "FROM event "
            "WHERE id=:event_id;",
            {"event_id": int(event_id)},
        )

        if not row:
            return None

        today: date = date.today()

        r = row
        event = Event(
            eid=r["id"],
            title=r["title"],
            description=r["description"],
            edate=date(
                day=r["event_day"],
                month=r["event_month"],
                year=today.year,
            ),
            voice_id=r["voice_id"],
            start_hour=-1,
            duration=2,
        )

        if event.edate < today:
            event.edate = event.edate.replace(year=today.year + 1)

        return event
