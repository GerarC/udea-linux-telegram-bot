from activity.domain.api.all_time_ranking_service import AllTimeRankingService
from activity.domain.model.user_activity import UserActivity
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.constants import DEFAULT_RANKING_LIMIT


class AllTimeRankingUsecase(AllTimeRankingService):
    def __init__(self, repository_port: ActivityRepositoryPort, ranking_limit: int = DEFAULT_RANKING_LIMIT) -> None:
        self._repository_port = repository_port
        self._ranking_limit = ranking_limit

    async def get_all_time_ranking(self, chat_id: int, limit: int | None = None) -> list[UserActivity]:
        return await self._repository_port.get_all_time_ranking(chat_id, limit or self._ranking_limit)
