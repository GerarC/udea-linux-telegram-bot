import asyncpg

from common.infrastructure.output.postgres.utils.constants import CREATE_GROUP_MEMBERS_SQL


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_GROUP_MEMBERS_SQL)
