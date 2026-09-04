from typing import Protocol

from news.domain.model.news_item import NewsItem


class NewsFeedPort(Protocol):
    """Outbound port: retrieves the available news items."""

    async def fetch(self) -> list[NewsItem]: ...
