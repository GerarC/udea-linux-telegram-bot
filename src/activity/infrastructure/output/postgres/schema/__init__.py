import asyncpg

from activity.infrastructure.output.postgres.schema.chat_activity_timeline import (
    ensure_schema as ensure_chat_activity_timeline_schema,
)
from activity.infrastructure.output.postgres.schema.user_message_stats import (
    ensure_schema as ensure_user_message_stats_schema,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    await ensure_user_message_stats_schema(pool)
    await ensure_chat_activity_timeline_schema(pool)
