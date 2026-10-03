from typing import Protocol

from banter.domain.model.banter_stat import BanterStat


class BanterStatsPort(Protocol):
    """Outbound port for recording and reading per-user banter stats."""

    async def record_insult(self, chat_id: int, user_id: int, username: str, full_name: str) -> None: ...

    async def record_compliment(self, chat_id: int, user_id: int, username: str, full_name: str) -> None: ...

    async def get_stats(self, chat_id: int, user_id: int) -> BanterStat | None: ...

    async def get_most_insulted(self, chat_id: int) -> BanterStat | None: ...

    async def get_most_complimented(self, chat_id: int) -> BanterStat | None: ...
