from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort
from points.domain.api.points_service import PointsService


class PointsUserInfoProvider(UserInfoProviderPort):
    """Adapts PointsService into a UserInfoProviderPort section for /usuario_info."""

    def __init__(self, points_service: PointsService) -> None:
        self._points_service = points_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        entry = await self._points_service.get_points(chat_id, user_id, username)
        if entry.user_points.points == 0:
            return None

        lines = [f"Autispuntos: {entry.user_points.points}", f"Nivel de autismo: {entry.level_label}"]
        position = await self._points_service.get_position(chat_id, user_id)
        if position is not None:
            lines.append(f"Posición en el ranking: #{position}")
        return UserInfoSection(title="🧠 Autispuntos", lines=lines)
