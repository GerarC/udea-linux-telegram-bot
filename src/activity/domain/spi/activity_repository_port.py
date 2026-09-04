from datetime import date
from typing import Protocol

from activity.domain.model.user_activity import UserActivity


class ActivityRepositoryPort(Protocol):
    """Outbound port: persists and reads per-chat, per-user message counts, broken down by month."""

    async def register_message(
        self, chat_id: int, user_id: int, username: str, period_month: date, hour_of_day: int, weekday: int
    ) -> None: ...

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

    async def get_chat_monthly_totals(self, chat_id: int, period_month: date) -> tuple[int, int]:
        """Returns (total_messages, distinct_participants) for the whole chat that month."""
        ...

    async def get_chat_all_time_total(self, chat_id: int) -> int: ...

    async def get_peak_hour(self, chat_id: int) -> int | None:
        """Returns the hour of day (0-23, local time) with the most messages ever, or None if empty."""
        ...

    async def get_peak_weekday(self, chat_id: int) -> int | None:
        """Returns the weekday (0=Monday..6=Sunday, local time) with the most messages ever, or None if empty."""
        ...
