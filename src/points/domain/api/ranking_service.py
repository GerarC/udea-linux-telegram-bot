from typing import Protocol

from points.domain.model.ranking_entry import RankingEntry


class RankingService(Protocol):
    """Inbound port for the points feature: chat-wide ranking."""

    async def get_ranking(self, chat_id: int, limit: int | None = None) -> list[RankingEntry]: ...
