import asyncio
import logging
import time

import feedparser

from news.domain.model.news_item import NewsItem
from news.domain.spi.news_feed_port import NewsFeedPort


class RssFeedAdapter(NewsFeedPort):
    """Implements NewsFeedPort by reading RSS feeds with feedparser, with an in-memory cache."""

    def __init__(self, feeds: list[str], ttl_seconds: int, entries_per_source: int) -> None:
        self._feeds = feeds
        self._ttl_seconds = ttl_seconds
        self._entries_per_source = entries_per_source
        self._cache: list[NewsItem] = []
        self._cache_at: float = 0.0
        self._lock = asyncio.Lock()

    async def fetch(self) -> list[NewsItem]:
        async with self._lock:
            if not self._cache or (time.monotonic() - self._cache_at) > self._ttl_seconds:
                fetched = await asyncio.to_thread(self._fetch_feeds)
                if fetched:
                    self._cache, self._cache_at = fetched, time.monotonic()
            return list(self._cache)

    def _fetch_feeds(self) -> list[NewsItem]:
        """Downloads the feeds. Blocking: called inside a thread."""
        items: list[NewsItem] = []
        for url in self._feeds:
            try:
                parsed = feedparser.parse(url)
            except Exception:
                logging.exception("Could not read feed %s", url)
                continue
            source = parsed.feed.get("title", url)
            for entry in parsed.entries[: self._entries_per_source]:
                title, link = entry.get("title"), entry.get("link")
                if title and link:
                    items.append(NewsItem(title.strip(), link.strip(), source))
        logging.info("Loaded feeds: %d news items", len(items))
        return items
