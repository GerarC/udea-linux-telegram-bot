from datetime import UTC, datetime

import asyncpg

from news.domain.spi.news_history_port import NewsHistoryPort

GET_LAST_FIRED_SQL = "SELECT last_fired_at FROM news_chat_state WHERE chat_id = $1"

MARK_FIRED_SQL = """
INSERT INTO news_chat_state (chat_id, last_fired_at)
VALUES ($1, now())
ON CONFLICT (chat_id) DO UPDATE SET last_fired_at = now()
"""

GET_RECENT_SQL = """
SELECT link FROM news_sent_links
WHERE chat_id = $1
ORDER BY sent_at DESC
LIMIT $2
"""

MARK_SENT_SQL = """
INSERT INTO news_sent_links (chat_id, link)
VALUES ($1, $2)
ON CONFLICT (chat_id, link) DO UPDATE SET sent_at = now()
"""

PRUNE_SENT_LINKS_SQL = """
DELETE FROM news_sent_links
WHERE chat_id = $1 AND link NOT IN (
    SELECT link FROM news_sent_links WHERE chat_id = $1 ORDER BY sent_at DESC LIMIT $2
)
"""


class PostgresNewsHistoryAdapter(NewsHistoryPort):
    """Implements NewsHistoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool, cooldown_seconds: int, recent_memory: int) -> None:
        self._pool = pool
        self._cooldown_seconds = cooldown_seconds
        self._recent_memory = recent_memory

    async def is_cooldown_active(self, chat_id: int) -> bool:
        async with self._pool.acquire() as conn:
            last_fired_at = await conn.fetchval(GET_LAST_FIRED_SQL, chat_id)
        if last_fired_at is None:
            return False
        elapsed = (datetime.now(UTC) - last_fired_at).total_seconds()
        return elapsed < self._cooldown_seconds

    async def mark_fired(self, chat_id: int) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(MARK_FIRED_SQL, chat_id)

    async def get_recent(self, chat_id: int) -> list[str]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_RECENT_SQL, chat_id, self._recent_memory)
        return [row["link"] for row in rows]

    async def mark_sent(self, chat_id: int, link: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(MARK_SENT_SQL, chat_id, link)
            await conn.execute(PRUNE_SENT_LINKS_SQL, chat_id, self._recent_memory)
