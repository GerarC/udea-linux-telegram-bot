from points.domain.api.user_points_service import UserPointsService
from points.domain.model.ranking_entry import RankingEntry
from points.domain.model.user_points import UserPoints
from points.domain.spi.points_repository_port import PointsRepositoryPort
from points.domain.utils.leveling import level_for


class UserPointsUsecase(UserPointsService):
    def __init__(self, repository_port: PointsRepositoryPort) -> None:
        self._repository_port = repository_port

    async def get_points(self, chat_id: int, user_id: int, username: str) -> RankingEntry:
        user_points = await self._repository_port.get_points(chat_id, user_id)
        if user_points is None:
            user_points = UserPoints(user_id=user_id, username=username, points=0)
        return RankingEntry(user_points=user_points, level_label=level_for(user_points.points))
