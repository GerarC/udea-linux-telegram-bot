from banter.domain.api.top_banter_stats_service import TopBanterStatsService
from banter.domain.model.top_banter_stats import TopBanterStats
from banter.domain.spi.banter_stats_port import BanterStatsPort


class TopBanterStatsUsecase(TopBanterStatsService):
    def __init__(self, stats_port: BanterStatsPort) -> None:
        self._stats_port = stats_port

    async def get_top(self, chat_id: int) -> TopBanterStats:
        most_insulted = await self._stats_port.get_most_insulted(chat_id)
        most_complimented = await self._stats_port.get_most_complimented(chat_id)
        return TopBanterStats(most_insulted=most_insulted, most_complimented=most_complimented)
