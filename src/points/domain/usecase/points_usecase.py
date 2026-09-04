from points.domain.model.grant_result import GrantResult
from points.domain.model.ranking_entry import RankingEntry
from points.domain.model.user_points import UserPoints
from points.domain.spi.points_repository_port import PointsRepositoryPort
from points.domain.utils.constants import DEFAULT_RANKING_LIMIT, LEVEL_THRESHOLDS


class PointsUsecase:
    def __init__(self, repository_port: PointsRepositoryPort, ranking_limit: int = DEFAULT_RANKING_LIMIT) -> None:
        self._repository_port = repository_port
        self._ranking_limit = ranking_limit

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
        ranking = await self.get_ranking(chat_id)
        return GrantResult(target=target, level_label=self._level_for(target.points), ranking=ranking)

    async def get_ranking(self, chat_id: int, limit: int | None = None) -> list[RankingEntry]:
        ranking = await self._repository_port.get_ranking(chat_id, limit or self._ranking_limit)
        return [RankingEntry(user_points=up, level_label=self._level_for(up.points)) for up in ranking]

    async def get_points(self, chat_id: int, user_id: int, username: str) -> RankingEntry:
        user_points = await self._repository_port.get_points(chat_id, user_id)
        if user_points is None:
            user_points = UserPoints(user_id=user_id, username=username, points=0)
        return RankingEntry(user_points=user_points, level_label=self._level_for(user_points.points))

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        return await self._repository_port.get_position(chat_id, user_id)

    @staticmethod
    def _level_for(points: int) -> str:
        for threshold, label in LEVEL_THRESHOLDS:
            if points >= threshold:
                return label
        return LEVEL_THRESHOLDS[-1][1]
