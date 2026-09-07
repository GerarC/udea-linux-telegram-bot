from typing import Protocol


class MonthlyStatsService(Protocol):
    """Inbound port for the activity feature: one user's stats for the current calendar month."""

    async def get_monthly_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        """Returns (message_count, 1-based rank) for this user this month, or None if they haven't posted."""
        ...
