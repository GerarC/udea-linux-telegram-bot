from typing import Protocol

from activity.domain.model.group_stats import GroupStats
from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry
from activity.domain.model.user_activity import UserActivity


class ActivityService(Protocol):
    """Inbound port for the activity feature."""

    async def register_message(self, chat_id: int, user_id: int, username: str) -> None: ...

    async def get_monthly_ranking(self, chat_id: int, limit: int | None = None) -> list[MonthlyRankingEntry]:
        """Ranking for the current calendar month, with each entry's position last month (if any)."""
        ...

    async def get_all_time_ranking(self, chat_id: int, limit: int | None = None) -> list[UserActivity]: ...

    async def get_monthly_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        """Returns (message_count, 1-based rank) for this user this month, or None if they haven't posted."""
        ...

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        """Returns (message_count, 1-based rank) for this user overall, or None if they never posted."""
        ...

    async def get_group_stats(self, chat_id: int) -> GroupStats: ...
