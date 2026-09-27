import asyncpg

from banter.domain.utils.constants import LEGACY_CHAT_ID
from banter.infrastructure.output.postgres.utils.constants import (
    ADD_INSULTS_CHAT_ID_COLUMN_SQL,
    ALTER_INSULTS_CHAT_ID_NOT_NULL_SQL,
    BACKFILL_INSULTS_CHAT_ID_SQL,
    CREATE_INSULTS_CHAT_ID_INDEX_SQL,
    CREATE_INSULTS_TABLE_SQL,
    HAS_INSULTS_CHAT_ID_COLUMN_SQL,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(CREATE_INSULTS_TABLE_SQL)

        has_chat_id = await conn.fetchval(HAS_INSULTS_CHAT_ID_COLUMN_SQL)
        if not has_chat_id:
            await conn.execute(ADD_INSULTS_CHAT_ID_COLUMN_SQL)
            await conn.execute(BACKFILL_INSULTS_CHAT_ID_SQL, LEGACY_CHAT_ID)
            await conn.execute(ALTER_INSULTS_CHAT_ID_NOT_NULL_SQL)

        await conn.execute(CREATE_INSULTS_CHAT_ID_INDEX_SQL)
