import asyncpg

CREATE_INSULTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banter_insults (
    id SERIAL PRIMARY KEY,
    phrase TEXT NOT NULL
)
"""

CREATE_COMPLIMENTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banter_compliments (
    id SERIAL PRIMARY KEY,
    phrase TEXT NOT NULL
)
"""


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(CREATE_INSULTS_TABLE_SQL)
        await conn.execute(CREATE_COMPLIMENTS_TABLE_SQL)
