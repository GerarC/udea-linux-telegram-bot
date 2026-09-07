import asyncpg

from banter.infrastructure.output.postgres.utils.constants import CREATE_INSULTS_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_INSULTS_TABLE_SQL)
