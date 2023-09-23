import re
from typing import Any, Final, Mapping, Sequence

from psycopg import AsyncConnection


class Database:
    def __init__(self, connection: AsyncConnection) -> None:
        self.conn: Final[AsyncConnection] = connection
        self.param_re: Final = re.compile(r"(:[_\w]+)")

    async def _execute(self, cursor: Any, query: str, values: Mapping[str, Any]) -> Any:
        columns = self.param_re.findall(query)
        values_list = []
        for column in columns:
            query = query.replace(column, "%s")
            values_list.append(values[column[1:]])

        await cursor.execute(query, tuple(values_list))
        return cursor

    async def fetch_val(self, query: str, values: Mapping[str, Any]) -> Any:
        async with self.conn.cursor() as cur:
            cur = await self._execute(cur, query, values)
            res = await cur.fetchone()

        if not res:
            return None

        if isinstance(res, Sequence) and not isinstance(res, str):
            return res[0]

        return res
