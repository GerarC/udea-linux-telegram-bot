import asyncpg

from confessions.infrastructure.output.postgres.utils.constants import (
    CREATE_CONFESSION_TITLES_TABLE_SQL,
    SEED_CONFESSION_TITLES_SQL,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_CONFESSION_TITLES_TABLE_SQL)
        await conn.execute(SEED_CONFESSION_TITLES_SQL)
