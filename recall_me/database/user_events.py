from datetime import date
from typing import Final

from .interfaces import DatabaseAll
from .types import Event


class UserEvents:
    def __init__(self, database: DatabaseAll) -> None:
        self.database: Final[DatabaseAll] = database

    async def get_user_events(
        self,
        user_id: str,
        *,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Event]:
        rows = await self.database.fetch_all(
            "SELECT id, title, description, event_day, event_month, voice_id "
            "FROM event "
            "WHERE author_id=:user_id;",
            {"user_id": user_id},
        )

        today: date = date.today()

        events = [
            Event(
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
            for r in rows
        ]

        for event in events:
            if event.edate < today:
                event.edate = event.edate.replace(year=today.year + 1)

        from_date = from_date or today
        to_date = to_date or today.replace(year=today.year + 1)

        events = [e for e in events if from_date <= e.edate <= to_date]

        events.sort(key=lambda e: e.edate)
        return events
