import time

from news.domain.spi.news_history_port import NewsHistoryPort


class InMemoryHistoryAdapter(NewsHistoryPort):
    """Implements NewsHistoryPort in process memory.

    Natural place to swap in a database-backed implementation
    (e.g. SQLite) without touching the domain.
    """

    def __init__(self, cooldown_seconds: int, recent_memory: int) -> None:
        self._cooldown_seconds = cooldown_seconds
        self._recent_memory = recent_memory
        self._last_fired: dict[int, float] = {}
        self._recent: dict[int, list[str]] = {}

    def is_cooldown_active(self, chat_id: int) -> bool:
        elapsed = time.monotonic() - self._last_fired.get(chat_id, 0.0)
        return elapsed < self._cooldown_seconds

    def mark_fired(self, chat_id: int) -> None:
        self._last_fired[chat_id] = time.monotonic()

    def get_recent(self, chat_id: int) -> list[str]:
        return list(self._recent.setdefault(chat_id, []))

    def mark_sent(self, chat_id: int, link: str) -> None:
        seen = self._recent.setdefault(chat_id, [])
        seen.append(link)
        del seen[: -self._recent_memory]
