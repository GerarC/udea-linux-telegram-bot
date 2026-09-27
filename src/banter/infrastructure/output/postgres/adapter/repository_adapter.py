import asyncpg

from banter.domain.spi.banter_phrase_port import BanterPhrasePort
from banter.infrastructure.output.postgres.utils.constants import (
    ADD_COMPLIMENT_SQL,
    ADD_INSULT_SQL,
    GET_RANDOM_COMPLIMENT_SQL,
    GET_RANDOM_INSULT_SQL,
)


class PostgresBanterRepository(BanterPhrasePort):
    """Implements BanterPhrasePort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_random_insult(self, chat_id: int) -> str:
        async with self._pool.acquire() as conn:
            phrase = await conn.fetchval(GET_RANDOM_INSULT_SQL, chat_id)
        return phrase or ""

    async def get_random_compliment(self, chat_id: int) -> str:
        async with self._pool.acquire() as conn:
            phrase = await conn.fetchval(GET_RANDOM_COMPLIMENT_SQL, chat_id)
        return phrase or ""

    async def add_insult(self, chat_id: int, phrase: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(ADD_INSULT_SQL, chat_id, phrase)

    async def add_compliment(self, chat_id: int, phrase: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(ADD_COMPLIMENT_SQL, chat_id, phrase)
