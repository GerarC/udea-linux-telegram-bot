import asyncpg

from banter.infrastructure.output.postgres.schema.banter_compliments import (
    ensure_schema as ensure_banter_compliments_schema,
)
from banter.infrastructure.output.postgres.schema.banter_insults import ensure_schema as ensure_banter_insults_schema


async def ensure_schema(pool: asyncpg.Pool) -> None:
    await ensure_banter_insults_schema(pool)
    await ensure_banter_compliments_schema(pool)
