import asyncpg

from banter.domain.model.banter_stat import BanterStat
from banter.domain.spi.banter_stats_port import BanterStatsPort
from banter.infrastructure.output.postgres.utils.constants import (
    GET_BANTER_STATS_SQL,
    GET_MOST_COMPLIMENTED_SQL,
    GET_MOST_INSULTED_SQL,
    RECORD_COMPLIMENT_SQL,
    RECORD_INSULT_SQL,
)
from common.infrastructure.output.postgres.utils.helpers import upsert_member


def _row_to_stat(user_id: int, row: asyncpg.Record) -> BanterStat:
    return BanterStat(
        user_id=user_id,
        username=row["username"],
        full_name=row["full_name"],
        insults_received=row["insults_received"],
        compliments_received=row["compliments_received"],
    )


class PostgresBanterStatsRepository(BanterStatsPort):
    """Implements BanterStatsPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def record_insult(self, chat_id: int, user_id: int, username: str, full_name: str) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username, full_name)
            await conn.execute(RECORD_INSULT_SQL, chat_id, user_id)

    async def record_compliment(self, chat_id: int, user_id: int, username: str, full_name: str) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username, full_name)
            await conn.execute(RECORD_COMPLIMENT_SQL, chat_id, user_id)

    async def get_stats(self, chat_id: int, user_id: int) -> BanterStat | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_BANTER_STATS_SQL, chat_id, user_id)
        return _row_to_stat(user_id, row) if row else None

    async def get_most_insulted(self, chat_id: int) -> BanterStat | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_MOST_INSULTED_SQL, chat_id)
        return _row_to_stat(row["user_id"], row) if row else None

    async def get_most_complimented(self, chat_id: int) -> BanterStat | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_MOST_COMPLIMENTED_SQL, chat_id)
        return _row_to_stat(row["user_id"], row) if row else None
