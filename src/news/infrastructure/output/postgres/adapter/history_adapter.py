import asyncpg

from news.domain.spi.news_history_port import NewsHistoryPort
from news.infrastructure.output.postgres.utils.constants import (
    GET_RECENT_SQL,
    MARK_SENT_SQL,
    PRUNE_SENT_LINKS_SQL,
    TRY_FIRE_SQL,
)


class PostgresNewsHistoryAdapter(NewsHistoryPort):
    """Implements NewsHistoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool, cooldown_seconds: int, recent_memory: int) -> None:
        self._pool = pool
        self._cooldown_seconds = cooldown_seconds
        self._recent_memory = recent_memory

    async def try_fire(self, chat_id: int) -> bool:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(TRY_FIRE_SQL, chat_id, self._cooldown_seconds)
        return row is not None

    async def get_recent(self, chat_id: int) -> list[str]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_RECENT_SQL, chat_id, self._recent_memory)
        return [row["link"] for row in rows]

    async def mark_sent(self, chat_id: int, link: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(MARK_SENT_SQL, chat_id, link)
            await conn.execute(PRUNE_SENT_LINKS_SQL, chat_id, self._recent_memory)
