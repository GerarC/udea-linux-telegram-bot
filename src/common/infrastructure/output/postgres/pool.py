from collections.abc import AsyncIterator

import asyncpg

from common.infrastructure.output.postgres.schema import ensure_schema


async def init_pool(host: str, port: int, database: str, user: str, password: str) -> AsyncIterator[asyncpg.Pool]:
    # statement_cache_size=0: required for Supabase's pooler (PgBouncer in transaction
    # mode) - it doesn't support asyncpg's server-side prepared statement cache.
    pool = await asyncpg.create_pool(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        statement_cache_size=0,
    )
    # group_members must exist before any feature's own schema (they FK to it).
    await ensure_schema(pool)
    yield pool
    await pool.close()
