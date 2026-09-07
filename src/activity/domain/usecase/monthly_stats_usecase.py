from zoneinfo import ZoneInfo

from activity.domain.api.monthly_stats_service import MonthlyStatsService
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.clock import current_month
from activity.domain.utils.constants import DEFAULT_TIMEZONE


class MonthlyStatsUsecase(MonthlyStatsService):
    def __init__(self, repository_port: ActivityRepositoryPort, timezone: str = DEFAULT_TIMEZONE) -> None:
        self._repository_port = repository_port
        self._zone = ZoneInfo(timezone)

    async def get_monthly_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        return await self._repository_port.get_monthly_stats(chat_id, user_id, current_month(self._zone))
