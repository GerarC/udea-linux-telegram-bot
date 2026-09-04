import asyncpg

from banter.domain.spi.banter_phrase_port import BanterPhrasePort

GET_RANDOM_INSULT_SQL = "SELECT phrase FROM banter_insults ORDER BY random() LIMIT 1"
GET_RANDOM_COMPLIMENT_SQL = "SELECT phrase FROM banter_compliments ORDER BY random() LIMIT 1"


class PostgresBanterRepository(BanterPhrasePort):
    """Implements BanterPhrasePort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_random_insult(self) -> str:
        async with self._pool.acquire() as conn:
            phrase = await conn.fetchval(GET_RANDOM_INSULT_SQL)
        return phrase or ""

    async def get_random_compliment(self) -> str:
        async with self._pool.acquire() as conn:
            phrase = await conn.fetchval(GET_RANDOM_COMPLIMENT_SQL)
        return phrase or ""
