from typing import Protocol


class AllTimeStatsService(Protocol):
    """Inbound port for the activity feature: one user's all-time stats."""

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        """Returns (message_count, 1-based rank) for this user overall, or None if they never posted."""
        ...
