from points.domain.api.user_position_service import UserPositionService
from points.domain.spi.points_repository_port import PointsRepositoryPort


class UserPositionUsecase(UserPositionService):
    def __init__(self, repository_port: PointsRepositoryPort) -> None:
        self._repository_port = repository_port

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        return await self._repository_port.get_position(chat_id, user_id)
