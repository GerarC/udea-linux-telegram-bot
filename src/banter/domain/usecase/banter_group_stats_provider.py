from banter.domain.api.top_banter_stats_service import TopBanterStatsService
from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort


def _display_name(user_id: int, username: str) -> str:
    return f"@{username}" if username else str(user_id)


class BanterGroupStatsProvider(GroupStatsProviderPort):
    """Adapts TopBanterStatsService into a GroupStatsProviderPort line for /stats_grupo."""

    def __init__(self, top_banter_stats_service: TopBanterStatsService) -> None:
        self._top_banter_stats_service = top_banter_stats_service

    async def get_group_stat_line(self, chat_id: int) -> str | None:
        top = await self._top_banter_stats_service.get_top(chat_id)
        if top.most_insulted is None and top.most_complimented is None:
            return None

        parts = []
        if top.most_insulted is not None:
            name = _display_name(top.most_insulted.user_id, top.most_insulted.username)
            parts.append(f"más insultado: {name} ({top.most_insulted.insults_received} veces)")
        if top.most_complimented is not None:
            name = _display_name(top.most_complimented.user_id, top.most_complimented.username)
            parts.append(f"más halagado: {name} ({top.most_complimented.compliments_received} veces)")
        return "😈 Banter: " + " · ".join(parts)
