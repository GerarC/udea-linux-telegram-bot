from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort
from points.domain.api.user_points_service import UserPointsService
from points.domain.api.user_position_service import UserPositionService


class PointsUserInfoProvider(UserInfoProviderPort):
    """Adapts UserPositionService + UserPointsService into a UserInfoProviderPort section for /usuario_info."""

    def __init__(self, user_position_service: UserPositionService, user_points_service: UserPointsService) -> None:
        self._user_position_service = user_position_service
        self._user_points_service = user_points_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        # NOTE: gate on get_position (None means no row at all), not points == 0 -
        # points can legitimately be exactly 0 with a real row (e.g. +5 then -5).
        position = await self._user_position_service.get_position(chat_id, user_id)
        if position is None:
            return None

        entry = await self._user_points_service.get_points(chat_id, user_id, username)
        lines = [
            f"Autispuntos: {entry.user_points.points}",
            f"Nivel de autismo: {entry.level_label}",
            f"Posición en el ranking: #{position}",
        ]
        return UserInfoSection(title="🧠 Autispuntos", lines=lines)
