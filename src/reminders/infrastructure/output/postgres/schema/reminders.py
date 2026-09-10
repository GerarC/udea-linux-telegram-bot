import asyncpg

from reminders.infrastructure.output.postgres.utils.constants import CREATE_REMINDERS_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_REMINDERS_TABLE_SQL)
