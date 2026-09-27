import asyncpg

from banter.infrastructure.output.postgres.utils.constants import (
    ADD_COMPLIMENTS_CHAT_ID_COLUMN_SQL,
    CREATE_COMPLIMENTS_CHAT_ID_INDEX_SQL,
    CREATE_COMPLIMENTS_TABLE_SQL,
    DELETE_ALL_COMPLIMENTS_SQL,
    HAS_COMPLIMENTS_CHAT_ID_COLUMN_SQL,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(CREATE_COMPLIMENTS_TABLE_SQL)

        has_chat_id = await conn.fetchval(HAS_COMPLIMENTS_CHAT_ID_COLUMN_SQL)
        if not has_chat_id:
            await conn.execute(DELETE_ALL_COMPLIMENTS_SQL)
            await conn.execute(ADD_COMPLIMENTS_CHAT_ID_COLUMN_SQL)

        await conn.execute(CREATE_COMPLIMENTS_CHAT_ID_INDEX_SQL)
