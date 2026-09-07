import asyncpg

from news.infrastructure.output.postgres.utils.constants import CREATE_NEWS_CHAT_STATE_TABLE_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_NEWS_CHAT_STATE_TABLE_SQL)
