from common.domain.model.group_stat_line import GroupStatLine, GroupStatMention
from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort
from points.domain.api.ranking_service import RankingService


class PointsGroupStatsProvider(GroupStatsProviderPort):
    """Adapts RankingService into GroupStatsProviderPort lines for /stats_grupo."""

    def __init__(self, ranking_service: RankingService) -> None:
        self._ranking_service = ranking_service

    async def get_group_stat_lines(self, chat_id: int) -> list[GroupStatLine]:
        ranking = await self._ranking_service.get_ranking(chat_id, limit=1)
        if not ranking:
            return []

        top = ranking[0]
        return [
            GroupStatLine(
                label="Más autista",
                value=f"({top.user_points.points} Autispuntos, {top.level_label})",
                mention=GroupStatMention(top.user_points.user_id, top.user_points.username, top.user_points.full_name),
            )
        ]
