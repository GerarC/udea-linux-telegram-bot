import asyncpg

from common.infrastructure.output.postgres.utils.constants import (
    ADD_FULL_NAME_COLUMN_SQL,
    CREATE_GROUP_MEMBERS_SQL,
    HAS_FULL_NAME_COLUMN_SQL,
    MOVE_LEGACY_USERNAMES_TO_FULL_NAME_SQL,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_GROUP_MEMBERS_SQL)
        async with conn.transaction():
            if not await conn.fetchval(HAS_FULL_NAME_COLUMN_SQL):
                await conn.execute(ADD_FULL_NAME_COLUMN_SQL)
                await conn.execute(MOVE_LEGACY_USERNAMES_TO_FULL_NAME_SQL)
