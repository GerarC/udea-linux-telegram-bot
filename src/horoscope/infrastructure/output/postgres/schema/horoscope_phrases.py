import asyncpg

from horoscope.infrastructure.output.postgres.utils.constants import CREATE_HOROSCOPE_PHRASES_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_HOROSCOPE_PHRASES_TABLE_SQL)
