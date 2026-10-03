from typing import Protocol

from common.domain.model.group_stat_line import GroupStatLine


class GroupStatsProviderPort(Protocol):
    """Implemented by any feature that wants to contribute extra lines to /stats_grupo."""

    async def get_group_stat_lines(self, chat_id: int) -> list[GroupStatLine]:
        """Returns an empty list when the feature has nothing to show for this chat yet."""
        ...
