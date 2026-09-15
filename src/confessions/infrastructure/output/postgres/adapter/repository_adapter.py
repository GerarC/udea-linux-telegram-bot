import asyncpg

from common.infrastructure.output.postgres.utils.helpers import upsert_member
from confessions.domain.model.confession import Confession
from confessions.domain.spi.confession_repository_port import ConfessionRepositoryPort
from confessions.infrastructure.output.postgres.utils.constants import (
    CREATE_CONFESSION_SQL,
    GET_RECENT_CONFESSIONS_SQL,
    SOFT_DELETE_CONFESSION_SQL,
)


def _to_confession(row: asyncpg.Record) -> Confession:
    return Confession(
        id=row["id"],
        chat_id=row["chat_id"],
        user_id=row["user_id"],
        content=row["content"],
        created_at=row["created_at"],
        is_deleted=row["is_deleted"],
    )


class PostgresConfessionRepository(ConfessionRepositoryPort):
    """Implements ConfessionRepositoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create_confession(self, chat_id: int, user_id: int, username: str, content: str) -> Confession:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username)
            row = await conn.fetchrow(CREATE_CONFESSION_SQL, chat_id, user_id, content)
        return _to_confession(row)

    async def get_recent_confessions(self, chat_id: int, limit: int) -> list[Confession]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_RECENT_CONFESSIONS_SQL, chat_id, limit)
        return [_to_confession(row) for row in rows]

    async def soft_delete_confession(self, chat_id: int, confession_id: int) -> Confession | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(SOFT_DELETE_CONFESSION_SQL, confession_id, chat_id)
        return _to_confession(row) if row is not None else None
