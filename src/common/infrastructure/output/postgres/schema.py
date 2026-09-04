import asyncpg

CREATE_GROUP_MEMBERS_SQL = """
CREATE TABLE IF NOT EXISTS group_members (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    username TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (chat_id, user_id)
)
"""


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_GROUP_MEMBERS_SQL)
