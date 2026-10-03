from banter.domain.api.top_banter_stats_service import TopBanterStatsService
from common.domain.model.group_stat_line import GroupStatLine, GroupStatMention
from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort


class BanterGroupStatsProvider(GroupStatsProviderPort):
    """Adapts TopBanterStatsService into GroupStatsProviderPort lines for /stats_grupo."""

    def __init__(self, top_banter_stats_service: TopBanterStatsService) -> None:
        self._top_banter_stats_service = top_banter_stats_service

    async def get_group_stat_lines(self, chat_id: int) -> list[GroupStatLine]:
        top = await self._top_banter_stats_service.get_top(chat_id)

        lines = []
        if top.most_insulted is not None:
            lines.append(
                GroupStatLine(
                    label="Más insultado",
                    value=f"({top.most_insulted.insults_received} veces)",
                    mention=GroupStatMention(
                        top.most_insulted.user_id, top.most_insulted.username, top.most_insulted.full_name
                    ),
                )
            )
        if top.most_complimented is not None:
            lines.append(
                GroupStatLine(
                    label="Más halagado",
                    value=f"({top.most_complimented.compliments_received} veces)",
                    mention=GroupStatMention(
                        top.most_complimented.user_id, top.most_complimented.username, top.most_complimented.full_name
                    ),
                )
            )
        return lines
