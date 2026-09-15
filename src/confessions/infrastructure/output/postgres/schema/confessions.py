import asyncpg

from confessions.infrastructure.output.postgres.utils.constants import CREATE_CONFESSIONS_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_CONFESSIONS_TABLE_SQL)
