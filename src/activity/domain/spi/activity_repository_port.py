from datetime import date
from typing import Protocol

from activity.domain.model.user_activity import UserActivity


class ActivityRepositoryPort(Protocol):
    """Outbound port: persists and reads per-chat, per-user message counts, broken down by month."""

    async def register_message(self, chat_id: int, user_id: int, username: str, period_month: date) -> None: ...

    async def get_monthly_ranking(
        self, chat_id: int, period_month: date, limit: int | None = None
    ) -> list[UserActivity]:
        """Returns entries ordered by message_count desc. limit=None returns every user for that month."""
        ...

    async def get_all_time_ranking(self, chat_id: int, limit: int) -> list[UserActivity]: ...

    async def get_monthly_stats(self, chat_id: int, user_id: int, period_month: date) -> tuple[int, int] | None:
        """Returns (message_count, 1-based rank) for this user that month, or None if they didn't post."""
        ...

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        """Returns (message_count, 1-based rank) for this user overall, or None if they never posted."""
        ...
