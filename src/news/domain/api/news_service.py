from typing import Protocol

from news.domain.model.news_item import NewsItem


class NewsService(Protocol):
    """Inbound port for the news feature."""

    async def handle_message(self, chat_id: int, text: str) -> NewsItem | None: ...
