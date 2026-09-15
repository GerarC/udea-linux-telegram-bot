import asyncpg

from confessions.infrastructure.output.postgres.schema.confession_titles import (
    ensure_schema as ensure_confession_titles_schema,
)
from confessions.infrastructure.output.postgres.schema.confessions import ensure_schema as ensure_confessions_schema


async def ensure_schema(pool: asyncpg.Pool) -> None:
    await ensure_confessions_schema(pool)
    await ensure_confession_titles_schema(pool)
