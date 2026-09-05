from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort
from points.domain.api.points_service import PointsService


class PointsGroupStatsProvider(GroupStatsProviderPort):
    """Adapts PointsService into a GroupStatsProviderPort line for /stats_grupo."""

    def __init__(self, points_service: PointsService) -> None:
        self._points_service = points_service

    async def get_group_stat_line(self, chat_id: int) -> str | None:
        ranking = await self._points_service.get_ranking(chat_id, limit=1)
        if not ranking:
            return None

        top = ranking[0]
        name = f"@{top.user_points.username}" if top.user_points.username else str(top.user_points.user_id)
        return f"Más autista: {name} ({top.user_points.points} Autispuntos, {top.level_label})"
