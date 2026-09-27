from datetime import date

from activity.domain.model.monthly_activity import MonthlyActivity


class FakeActivityRepository:
    """Minimal duck-typed stand-in for ActivityRepositoryPort - only implements what
    MonthlyHistoryUsecase actually calls."""

    def __init__(self, monthly_history: list[MonthlyActivity] | None = None) -> None:
        self._monthly_history = monthly_history or []

    async def get_chat_monthly_history(self, chat_id: int, since_month: date) -> list[MonthlyActivity]:
        return [entry for entry in self._monthly_history if entry.period_month >= since_month]
