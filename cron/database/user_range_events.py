from datetime import date
from typing import Final

from .interfaces import DatabaseAll
from .types import Event


def event_in_range(edate: date, *, from_date: date, to_date: date) -> bool:
    for ed in (
        edate,
        edate.replace(year=edate.year - 1),
        edate.replace(year=edate.year + 1),
    ):
        if from_date <= ed <= to_date:
            return True

    return False


class UserRangeEvents:
    def __init__(self, database: DatabaseAll) -> None:
        self.database: Final[DatabaseAll] = database

    async def get_user_events(
        self,
        user_id: str,
        from_date: date,
        to_date: date,
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

        events = [
            e
            for e in events
            if event_in_range(
                e.edate,
                from_date=from_date,
                to_date=to_date,
            )
        ]

        events.sort(key=lambda e: e.edate)
        return events
