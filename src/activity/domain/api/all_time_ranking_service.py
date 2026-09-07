from typing import Protocol

from activity.domain.model.user_activity import UserActivity


class AllTimeRankingService(Protocol):
    """Inbound port for the activity feature: all-time ranking."""

    async def get_all_time_ranking(self, chat_id: int, limit: int | None = None) -> list[UserActivity]: ...
