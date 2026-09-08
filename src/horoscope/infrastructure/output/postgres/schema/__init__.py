import asyncpg

from horoscope.infrastructure.output.postgres.schema.horoscope_phrases import (
    ensure_schema as ensure_horoscope_phrases_schema,
)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    await ensure_horoscope_phrases_schema(pool)
