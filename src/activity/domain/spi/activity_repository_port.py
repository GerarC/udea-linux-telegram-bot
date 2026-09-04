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
