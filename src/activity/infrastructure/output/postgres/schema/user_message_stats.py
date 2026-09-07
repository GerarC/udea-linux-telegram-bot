import asyncpg

from activity.infrastructure.output.postgres.utils.constants import (
    CREATE_USER_MESSAGE_STATS_TABLE_SQL,
    DROP_LEGACY_USER_MESSAGE_STATS_TABLE_SQL,
    HAS_PERIOD_MONTH_COLUMN_SQL,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        has_period_month = await conn.fetchval(HAS_PERIOD_MONTH_COLUMN_SQL)
        if not has_period_month:
            await conn.execute(DROP_LEGACY_USER_MESSAGE_STATS_TABLE_SQL)
        await conn.execute(CREATE_USER_MESSAGE_STATS_TABLE_SQL)
