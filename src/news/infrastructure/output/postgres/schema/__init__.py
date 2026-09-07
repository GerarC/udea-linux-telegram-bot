import asyncpg

from news.infrastructure.output.postgres.schema.news_chat_state import ensure_schema as ensure_news_chat_state_schema
from news.infrastructure.output.postgres.schema.news_sent_links import ensure_schema as ensure_news_sent_links_schema


async def ensure_schema(pool: asyncpg.Pool) -> None:
    await ensure_news_chat_state_schema(pool)
    await ensure_news_sent_links_schema(pool)
