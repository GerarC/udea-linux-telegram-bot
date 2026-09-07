from datetime import date

import asyncpg

from activity.domain.model.user_activity import UserActivity
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.infrastructure.output.postgres.utils.constants import (
    GET_ALL_TIME_RANKING_SQL,
    GET_ALL_TIME_STATS_SQL,
    GET_CHAT_ALL_TIME_TOTAL_SQL,
    GET_CHAT_MONTHLY_TOTALS_SQL,
    GET_MONTHLY_RANKING_SQL,
    GET_MONTHLY_STATS_SQL,
    GET_PEAK_HOUR_SQL,
    GET_PEAK_WEEKDAY_SQL,
    REGISTER_DAILY_ACTIVITY_SQL,
    REGISTER_MESSAGE_SQL,
)
from common.infrastructure.output.postgres.utils.helpers import upsert_member


class PostgresActivityRepository(ActivityRepositoryPort):
    """Implements ActivityRepositoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def register_message(
        self, chat_id: int, user_id: int, username: str, period_month: date, hour_of_day: int, activity_date: date
    ) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username)
            await conn.execute(REGISTER_MESSAGE_SQL, chat_id, user_id, period_month)
            await conn.execute(REGISTER_DAILY_ACTIVITY_SQL, chat_id, activity_date, hour_of_day)

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

    async def get_monthly_stats(self, chat_id: int, user_id: int, period_month: date) -> tuple[int, int] | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_MONTHLY_STATS_SQL, chat_id, period_month, user_id)
        return (row["message_count"], row["rank"]) if row else None

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_ALL_TIME_STATS_SQL, chat_id, user_id)
        return (row["message_count"], row["rank"]) if row else None

    async def get_chat_monthly_totals(self, chat_id: int, period_month: date) -> tuple[int, int]:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_CHAT_MONTHLY_TOTALS_SQL, chat_id, period_month)
        return row["total"], row["participants"]

    async def get_chat_all_time_total(self, chat_id: int) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(GET_CHAT_ALL_TIME_TOTAL_SQL, chat_id)

    async def get_peak_hour(self, chat_id: int) -> int | None:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(GET_PEAK_HOUR_SQL, chat_id)

    async def get_peak_weekday(self, chat_id: int) -> int | None:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(GET_PEAK_WEEKDAY_SQL, chat_id)
