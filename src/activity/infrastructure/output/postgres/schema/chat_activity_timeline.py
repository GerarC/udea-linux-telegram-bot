import asyncpg

from activity.infrastructure.output.postgres.utils.constants import CREATE_CHAT_ACTIVITY_TIMELINE_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_CHAT_ACTIVITY_TIMELINE_TABLE_SQL)
