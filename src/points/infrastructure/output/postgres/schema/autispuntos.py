import asyncpg

from points.infrastructure.output.postgres.utils.constants import (
    ADD_MEMBER_FK_SQL,
    BACKFILL_MEMBERS_SQL,
    CREATE_AUTISPUNTOS_TABLE_SQL,
    DROP_USERNAME_COLUMN_SQL,
    HAS_USERNAME_COLUMN_SQL,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(CREATE_AUTISPUNTOS_TABLE_SQL)

        has_username = await conn.fetchval(HAS_USERNAME_COLUMN_SQL)
        if has_username:
            # One-time migration: keep existing points, move usernames to group_members.
            await conn.execute(BACKFILL_MEMBERS_SQL)
            await conn.execute(DROP_USERNAME_COLUMN_SQL)

        await conn.execute(ADD_MEMBER_FK_SQL)
