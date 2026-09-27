from banter.domain.api.user_banter_stats_service import UserBanterStatsService
from banter.domain.model.banter_stat import BanterStat
from banter.domain.spi.banter_stats_port import BanterStatsPort


class UserBanterStatsUsecase(UserBanterStatsService):
    def __init__(self, stats_port: BanterStatsPort) -> None:
        self._stats_port = stats_port

    async def get_stats(self, chat_id: int, user_id: int) -> BanterStat | None:
        return await self._stats_port.get_stats(chat_id, user_id)
