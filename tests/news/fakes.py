from news.domain.model.news_item import NewsItem
from news.domain.spi.news_feed_port import NewsFeedPort
from news.domain.spi.news_history_port import NewsHistoryPort


class FakeNewsFeedPort(NewsFeedPort):
    def __init__(self, items: list[NewsItem] | None = None) -> None:
        self.items = list(items or [])

    async def fetch(self) -> list[NewsItem]:
        return self.items


class FakeNewsHistoryPort(NewsHistoryPort):
    def __init__(self, can_fire: bool = True, recent: list[str] | None = None) -> None:
        self.can_fire = can_fire
        self.recent = list(recent or [])
        self.try_fire_calls: list[int] = []
        self.marked: list[tuple[int, str]] = []

    async def try_fire(self, chat_id: int) -> bool:
        self.try_fire_calls.append(chat_id)
        return self.can_fire

    async def get_recent(self, chat_id: int) -> list[str]:
        return self.recent

    async def mark_sent(self, chat_id: int, link: str) -> None:
        self.marked.append((chat_id, link))
