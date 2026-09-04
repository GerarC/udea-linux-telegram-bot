from typing import Protocol


class GroupStatsProviderPort(Protocol):
    """Implemented by any feature that wants to contribute an extra line to /stats_grupo."""

    async def get_group_stat_line(self, chat_id: int) -> str | None:
        """Returns None when the feature has nothing to show for this chat yet."""
        ...
