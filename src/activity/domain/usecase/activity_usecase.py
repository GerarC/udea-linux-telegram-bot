from zoneinfo import ZoneInfo

from activity.domain.api.activity_service import ActivityService
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.clock import now_in
from activity.domain.utils.constants import DEFAULT_TIMEZONE


class ActivityUsecase(ActivityService):
    def __init__(self, repository_port: ActivityRepositoryPort, timezone: str = DEFAULT_TIMEZONE) -> None:
        self._repository_port = repository_port
        self._zone = ZoneInfo(timezone)

    async def register_message(self, chat_id: int, user_id: int, username: str) -> None:
        now = now_in(self._zone)
        period_month = now.date().replace(day=1)
        await self._repository_port.register_message(
            chat_id, user_id, username, period_month, now.hour, now.date()
        )
