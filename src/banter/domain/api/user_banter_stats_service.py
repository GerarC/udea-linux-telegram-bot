from typing import Protocol

from banter.domain.model.banter_stat import BanterStat


class UserBanterStatsService(Protocol):
    """Inbound port for the banter feature: banter stats for one user in one chat."""

    async def get_stats(self, chat_id: int, user_id: int) -> BanterStat | None:
        """Returns None when the user has no banter_stats row yet."""
        ...
