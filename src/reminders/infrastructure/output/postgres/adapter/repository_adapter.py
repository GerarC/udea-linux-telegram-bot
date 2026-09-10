from datetime import datetime

import asyncpg

from common.infrastructure.output.postgres.utils.helpers import upsert_member
from reminders.domain.model.reminder import Reminder
from reminders.domain.spi.reminder_repository_port import ReminderRepositoryPort
from reminders.infrastructure.output.postgres.utils.constants import (
    CREATE_REMINDER_SQL,
    GET_PENDING_REMINDERS_SQL,
    TRY_FIRE_REMINDER_SQL,
)


def _to_reminder(row: asyncpg.Record) -> Reminder:
    return Reminder(
        id=row["id"],
        chat_id=row["chat_id"],
        user_id=row["user_id"],
        message=row["message"],
        remind_at=row["remind_at"],
        fired=row["fired"],
    )


class PostgresReminderRepository(ReminderRepositoryPort):
    """Implements ReminderRepositoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create_reminder(
        self, chat_id: int, user_id: int, username: str, message: str, remind_at: datetime
    ) -> Reminder:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username)
            row = await conn.fetchrow(CREATE_REMINDER_SQL, chat_id, user_id, message, remind_at)
        return _to_reminder(row)

    async def get_pending(self) -> list[Reminder]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_PENDING_REMINDERS_SQL)
        return [_to_reminder(row) for row in rows]

    async def try_fire(self, reminder_id: int) -> Reminder | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(TRY_FIRE_REMINDER_SQL, reminder_id)
        return _to_reminder(row) if row is not None else None
