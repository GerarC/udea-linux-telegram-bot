from typing import Protocol

from activity.domain.model.group_stats import GroupStats


class GroupStatsService(Protocol):
    """Inbound port for the activity feature: chat-wide stats for /stats_grupo."""

    async def get_group_stats(self, chat_id: int) -> GroupStats: ...
