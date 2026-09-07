from typing import Protocol

from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry


class MonthlyRankingService(Protocol):
    """Inbound port for the activity feature: ranking for the current calendar month."""

    async def get_monthly_ranking(self, chat_id: int, limit: int | None = None) -> list[MonthlyRankingEntry]:
        """Ranking for the current calendar month, with each entry's position last month (if any)."""
        ...
