import asyncpg

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS news_chat_state (
    chat_id BIGINT PRIMARY KEY,
    last_fired_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS news_sent_links (
    chat_id BIGINT NOT NULL,
    link TEXT NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (chat_id, link)
);
"""


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_TABLES_SQL)
