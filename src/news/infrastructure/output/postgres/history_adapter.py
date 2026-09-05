import asyncpg

from news.domain.spi.news_history_port import NewsHistoryPort

# NOTE: atomic check-and-set. ON CONFLICT locks the existing row before evaluating
# the WHERE clause, so under concurrent_updates two triggers racing on the same
# chat_id serialize: the second sees the first's just-committed last_fired_at and
# correctly fails the cooldown check instead of both slipping through.
TRY_FIRE_SQL = """
INSERT INTO news_chat_state (chat_id, last_fired_at)
VALUES ($1, now())
ON CONFLICT (chat_id) DO UPDATE
    SET last_fired_at = now()
    WHERE news_chat_state.last_fired_at <= now() - ($2::int * interval '1 second')
RETURNING chat_id
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
