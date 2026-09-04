import asyncio
import logging
import time

import feedparser

from news.domain.error.fetching_news_error import FetchingNewsError
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
                try:
                    fetched = await asyncio.to_thread(self._fetch_feeds)
                    self._cache, self._cache_at = fetched, time.monotonic()
                except FetchingNewsError:
                    if not self._cache:
                        raise
                    logging.exception(
                        "Feed fetch failed, serving stale cache",
                        extra={"event": "feed_fetch_failed_stale_cache", "cached_item_count": len(self._cache)},
                    )
            return list(self._cache)

    def _fetch_feeds(self) -> list[NewsItem]:
        """Downloads the feeds. Blocking: called inside a thread."""
        items: list[NewsItem] = []
        for url in self._feeds:
            try:
                parsed = feedparser.parse(url)
            except Exception:
                logging.exception(
                    "Could not read feed %s", url, extra={"event": "feed_read_error", "feed_url": url}
                )
                continue

            if parsed.bozo and not parsed.entries:
                logging.warning(
                    "Feed %s returned malformed/empty content: %s",
                    url,
                    parsed.get("bozo_exception"),
                    extra={
                        "event": "feed_malformed",
                        "feed_url": url,
                        "bozo_exception": str(parsed.get("bozo_exception")),
                    },
                )
                continue

            source = parsed.feed.get("title", url)
            source_item_count = 0
            for entry in parsed.entries[: self._entries_per_source]:
                title, link = entry.get("title"), entry.get("link")
                if title and link:
                    items.append(NewsItem(title.strip(), link.strip(), source))
                    source_item_count += 1

            logging.info(
                "Loaded feed %s: %d news items",
                source,
                source_item_count,
                extra={"event": "feed_loaded", "feed_url": url, "source": source, "item_count": source_item_count},
            )

        if not items and self._feeds:
            raise FetchingNewsError(f"Could not fetch any news item from {len(self._feeds)} feed(s)")

        logging.info(
            "Loaded feeds: %d news items",
            len(items),
            extra={"event": "feeds_loaded", "item_count": len(items), "feed_count": len(self._feeds)},
        )
        return items
