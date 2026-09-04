from datetime import date

import asyncpg

from activity.domain.model.user_activity import UserActivity
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from common.infrastructure.output.postgres.members import upsert_member

REGISTER_MESSAGE_SQL = """
INSERT INTO user_message_stats (chat_id, user_id, period_month, message_count)
VALUES ($1, $2, $3, 1)
ON CONFLICT (chat_id, user_id, period_month) DO UPDATE SET message_count = user_message_stats.message_count + 1
"""

GET_MONTHLY_RANKING_SQL = """
SELECT gm.user_id, gm.username, ums.message_count
FROM user_message_stats ums
JOIN group_members gm ON gm.chat_id = ums.chat_id AND gm.user_id = ums.user_id
WHERE ums.chat_id = $1 AND ums.period_month = $2
ORDER BY ums.message_count DESC
LIMIT $3
"""

GET_ALL_TIME_RANKING_SQL = """
SELECT gm.user_id, gm.username, SUM(ums.message_count)::bigint AS message_count
FROM user_message_stats ums
JOIN group_members gm ON gm.chat_id = ums.chat_id AND gm.user_id = ums.user_id
WHERE ums.chat_id = $1
GROUP BY gm.user_id, gm.username
ORDER BY message_count DESC
LIMIT $2
"""


class PostgresActivityRepository(ActivityRepositoryPort):
    """Implements ActivityRepositoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def register_message(self, chat_id: int, user_id: int, username: str, period_month: date) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username)
            await conn.execute(REGISTER_MESSAGE_SQL, chat_id, user_id, period_month)

    async def get_monthly_ranking(
        self, chat_id: int, period_month: date, limit: int | None = None
    ) -> list[UserActivity]:
        # NOTE: LIMIT NULL is Postgres shorthand for "no limit" - used to fetch every
        # user's position for a month when computing month-over-month movement.
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_MONTHLY_RANKING_SQL, chat_id, period_month, limit)
        return [
            UserActivity(user_id=row["user_id"], username=row["username"], message_count=row["message_count"])
            for row in rows
        ]

    async def get_all_time_ranking(self, chat_id: int, limit: int) -> list[UserActivity]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_ALL_TIME_RANKING_SQL, chat_id, limit)
        return [
            UserActivity(user_id=row["user_id"], username=row["username"], message_count=row["message_count"])
            for row in rows
        ]
