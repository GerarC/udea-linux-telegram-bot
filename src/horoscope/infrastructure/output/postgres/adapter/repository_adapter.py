import asyncpg

from horoscope.domain.spi.horoscope_phrase_port import HoroscopePhrasePort
from horoscope.infrastructure.output.postgres.utils.constants import GET_PHRASE_BY_OFFSET_SQL, GET_PHRASE_COUNT_SQL


class PostgresHoroscopeRepository(HoroscopePhrasePort):
    """Implements HoroscopePhrasePort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_phrase_count(self) -> int:
        async with self._pool.acquire() as conn:
            count = await conn.fetchval(GET_PHRASE_COUNT_SQL)
        return count or 0

    async def get_phrase(self, index: int) -> str:
        async with self._pool.acquire() as conn:
            phrase = await conn.fetchval(GET_PHRASE_BY_OFFSET_SQL, index)
        return phrase or ""
