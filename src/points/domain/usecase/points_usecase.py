from points.domain.api.points_service import PointsService
from points.domain.api.ranking_service import RankingService
from points.domain.model.grant_result import GrantResult
from points.domain.spi.points_repository_port import PointsRepositoryPort
from points.domain.utils.leveling import level_for


class PointsUsecase(PointsService):
    def __init__(self, repository_port: PointsRepositoryPort, ranking_service: RankingService) -> None:
        self._repository_port = repository_port
        self._ranking_service = ranking_service

    async def grant_points(
        self,
        chat_id: int,
        granter_is_admin: bool,
        target_id: int,
        target_username: str,
        amount: int,
    ) -> GrantResult | None:
        if not granter_is_admin:
            return None

        target = await self._repository_port.add_points(chat_id, target_id, target_username, amount)
        ranking = await self._ranking_service.get_ranking(chat_id)
        return GrantResult(target=target, level_label=level_for(target.points), ranking=ranking)
