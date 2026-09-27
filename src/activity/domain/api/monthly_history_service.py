from typing import Protocol

from activity.domain.model.monthly_activity import MonthlyActivity


class MonthlyHistoryService(Protocol):
    """Inbound port for the activity feature: message totals for the last few months."""

    async def get_monthly_history(self, chat_id: int) -> list[MonthlyActivity]:
        """Returns one entry per month, oldest first, including months with zero messages."""
        ...
