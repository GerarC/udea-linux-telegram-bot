import random
import re

from news.domain.model.news_item import NewsItem
from news.domain.spi.news_feed_port import NewsFeedPort
from news.domain.spi.news_history_port import NewsHistoryPort


class NewsUsecase:
    def __init__(
        self,
        feed_port: NewsFeedPort,
        history_port: NewsHistoryPort,
        trigger_pattern: re.Pattern[str],
    ) -> None:
        self._feed_port = feed_port
        self._history_port = history_port
        self._trigger_pattern = trigger_pattern

    async def handle_message(self, chat_id: int, text: str) -> NewsItem | None:
        if not self._trigger_pattern.search(text):
            return None
        if not await self._history_port.try_fire(chat_id):
            return None

        items = await self._feed_port.fetch()
        if not items:
            return None

        item = await self._pick_item(chat_id, items)
        await self._history_port.mark_sent(chat_id, item.link)
        return item

    async def _pick_item(self, chat_id: int, items: list[NewsItem]) -> NewsItem:
        """Picks a news item, avoiding the ones already sent to this chat."""
        seen = await self._history_port.get_recent(chat_id)
        fresh = [i for i in items if i.link not in seen]
        return random.choice(fresh or items)
