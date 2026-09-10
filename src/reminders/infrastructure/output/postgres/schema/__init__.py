import asyncpg

from reminders.infrastructure.output.postgres.schema.reminders import ensure_schema as ensure_reminders_schema


async def ensure_schema(pool: asyncpg.Pool) -> None:
    await ensure_reminders_schema(pool)
