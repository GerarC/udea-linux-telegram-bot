from points.domain.api.ranking_service import RankingService
from points.domain.model.ranking_entry import RankingEntry
from points.domain.spi.points_repository_port import PointsRepositoryPort
from points.domain.utils.constants import DEFAULT_RANKING_LIMIT
from points.domain.utils.leveling import level_for


class RankingUsecase(RankingService):
    def __init__(self, repository_port: PointsRepositoryPort, ranking_limit: int = DEFAULT_RANKING_LIMIT) -> None:
        self._repository_port = repository_port
        self._ranking_limit = ranking_limit

    async def get_ranking(self, chat_id: int, limit: int | None = None) -> list[RankingEntry]:
        ranking = await self._repository_port.get_ranking(chat_id, limit or self._ranking_limit)
        return [RankingEntry(user_points=up, level_label=level_for(up.points)) for up in ranking]
