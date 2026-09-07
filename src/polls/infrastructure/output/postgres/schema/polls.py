import asyncpg

from polls.infrastructure.output.postgres.utils.constants import CREATE_POLLS_INDEX_SQL, CREATE_POLLS_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_POLLS_TABLE_SQL)
        await conn.execute(CREATE_POLLS_INDEX_SQL)
