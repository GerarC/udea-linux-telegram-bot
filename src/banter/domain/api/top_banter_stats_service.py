from typing import Protocol

from banter.domain.model.top_banter_stats import TopBanterStats


class TopBanterStatsService(Protocol):
    """Inbound port for the banter feature: the most insulted/complimented user in a chat."""

    async def get_top(self, chat_id: int) -> TopBanterStats: ...
