from dependency_injector import containers, providers

from news.domain.usecase.news_usecase import NewsUsecase
from news.domain.utils.constants import RECENT_MEMORY, TRIGGER_PATTERN
from news.infrastructure.configuration.settings import load_news_settings
from news.infrastructure.output.postgres.history_adapter import PostgresNewsHistoryAdapter
from news.infrastructure.output.postgres.schema import ensure_schema
from news.infrastructure.output.rss.feed_adapter import RssFeedAdapter
from news.infrastructure.utils.constants import FEED_ENTRIES_PER_SOURCE

_settings = load_news_settings()


async def _ensure_news_schema(pool):
    await ensure_schema(pool)
    yield None


class NewsContainer(containers.DeclarativeContainer):
    """Wiring for the news feature: builds the adapters and exposes domain.api.NewsService."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_news_schema, pool=pool)

    feed_port = providers.Singleton(
        RssFeedAdapter,
        feeds=_settings.feeds,
        ttl_seconds=_settings.feed_ttl_seconds,
        entries_per_source=FEED_ENTRIES_PER_SOURCE,
    )

    history_port = providers.Singleton(
        PostgresNewsHistoryAdapter,
        pool=pool,
        cooldown_seconds=_settings.cooldown_seconds,
        recent_memory=RECENT_MEMORY,
    )

    usecase = providers.Factory(
        NewsUsecase,
        feed_port=feed_port,
        history_port=history_port,
        trigger_pattern=TRIGGER_PATTERN,
    )
