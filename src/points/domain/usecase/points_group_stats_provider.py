from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort
from points.domain.api.ranking_service import RankingService


class PointsGroupStatsProvider(GroupStatsProviderPort):
    """Adapts RankingService into a GroupStatsProviderPort line for /stats_grupo."""

    def __init__(self, ranking_service: RankingService) -> None:
        self._ranking_service = ranking_service

    async def get_group_stat_line(self, chat_id: int) -> str | None:
        ranking = await self._ranking_service.get_ranking(chat_id, limit=1)
        if not ranking:
            return None

        top = ranking[0]
        name = f"@{top.user_points.username}" if top.user_points.username else str(top.user_points.user_id)
        return f"Más autista: {name} ({top.user_points.points} Autispuntos, {top.level_label})"
