import asyncpg

from common.infrastructure.output.postgres.utils.helpers import upsert_member
from polls.domain.spi.poll_repository_port import PollRepositoryPort
from polls.infrastructure.output.postgres.utils.constants import (
    GET_CHAT_POLL_COUNT_SQL,
    GET_POLL_COUNT_SQL,
    SAVE_POLL_SQL,
)


class PostgresPollRepository(PollRepositoryPort):
    """Implements PollRepositoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def save_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username)
            await conn.execute(SAVE_POLL_SQL, chat_id, user_id, question)

    async def get_poll_count(self, chat_id: int, user_id: int) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(GET_POLL_COUNT_SQL, chat_id, user_id)

    async def get_chat_poll_count(self, chat_id: int) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(GET_CHAT_POLL_COUNT_SQL, chat_id)
