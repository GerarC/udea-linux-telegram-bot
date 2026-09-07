from activity.domain.api.all_time_stats_service import AllTimeStatsService
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort


class AllTimeStatsUsecase(AllTimeStatsService):
    def __init__(self, repository_port: ActivityRepositoryPort) -> None:
        self._repository_port = repository_port

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        return await self._repository_port.get_all_time_stats(chat_id, user_id)
