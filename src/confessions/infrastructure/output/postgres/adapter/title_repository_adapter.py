import asyncpg

from confessions.domain.model.confession_title import ConfessionTitle
from confessions.domain.spi.confession_title_port import ConfessionTitlePort
from confessions.infrastructure.output.postgres.utils.constants import GET_RANDOM_CONFESSION_TITLE_SQL


class PostgresConfessionTitleRepository(ConfessionTitlePort):
    """Implements ConfessionTitlePort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_random_title(self) -> ConfessionTitle:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_RANDOM_CONFESSION_TITLE_SQL)
        return ConfessionTitle(emoji=row["emoji"], title=row["title"], footer=row["footer"])
