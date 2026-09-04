import os
from dataclasses import dataclass

from news.domain.utils.constants import COOLDOWN_SECONDS
from news.infrastructure.utils.constants import FEED_TTL_SECONDS, FEEDS


@dataclass(frozen=True)
class NewsSettings:
    cooldown_seconds: int
    feed_ttl_seconds: int
    feeds: list[str]


def load_news_settings() -> NewsSettings:
    cooldown_seconds = int(os.environ.get("NEWS_COOLDOWN_SECONDS", COOLDOWN_SECONDS))
    feed_ttl_seconds = int(os.environ.get("NEWS_FEED_TTL_SECONDS", FEED_TTL_SECONDS))
    feeds = _parse_feeds(os.environ.get("NEWS_FEEDS"))
    return NewsSettings(cooldown_seconds=cooldown_seconds, feed_ttl_seconds=feed_ttl_seconds, feeds=feeds)


def _parse_feeds(raw: str | None) -> list[str]:
    if not raw:
        return FEEDS
    return [url.strip() for url in raw.split(",") if url.strip()]
