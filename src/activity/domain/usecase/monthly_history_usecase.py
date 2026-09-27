from zoneinfo import ZoneInfo

from activity.domain.api.monthly_history_service import MonthlyHistoryService
from activity.domain.model.monthly_activity import MonthlyActivity
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.clock import current_month, months_back
from activity.domain.utils.constants import DEFAULT_TIMEZONE, MONTHLY_HISTORY_WINDOW


class MonthlyHistoryUsecase(MonthlyHistoryService):
    def __init__(self, repository_port: ActivityRepositoryPort, timezone: str = DEFAULT_TIMEZONE) -> None:
        self._repository_port = repository_port
        self._zone = ZoneInfo(timezone)

    async def get_monthly_history(self, chat_id: int) -> list[MonthlyActivity]:
        current = current_month(self._zone)
        since = months_back(current, MONTHLY_HISTORY_WINDOW - 1)
        history = await self._repository_port.get_chat_monthly_history(chat_id, since)
        counts_by_month = {entry.period_month: entry.message_count for entry in history}

        # NOTE: the repository only returns months with at least one message - fill in
        # the gaps so the chart always shows a full, contiguous MONTHLY_HISTORY_WINDOW.
        months = [months_back(current, offset) for offset in range(MONTHLY_HISTORY_WINDOW - 1, -1, -1)]
        return [MonthlyActivity(period_month=month, message_count=counts_by_month.get(month, 0)) for month in months]
