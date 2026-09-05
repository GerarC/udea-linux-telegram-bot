from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort
from points.domain.api.points_service import PointsService


class PointsUserInfoProvider(UserInfoProviderPort):
    """Adapts PointsService into a UserInfoProviderPort section for /usuario_info."""

    def __init__(self, points_service: PointsService) -> None:
        self._points_service = points_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        # NOTE: gate on get_position (None means no row at all), not points == 0 -
        # points can legitimately be exactly 0 with a real row (e.g. +5 then -5).
        position = await self._points_service.get_position(chat_id, user_id)
        if position is None:
            return None

        entry = await self._points_service.get_points(chat_id, user_id, username)
        lines = [
            f"Autispuntos: {entry.user_points.points}",
            f"Nivel de autismo: {entry.level_label}",
            f"Posición en el ranking: #{position}",
        ]
        return UserInfoSection(title="🧠 Autispuntos", lines=lines)
