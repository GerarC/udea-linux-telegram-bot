from typing import Protocol

from points.domain.model.ranking_entry import RankingEntry


class UserPointsService(Protocol):
    """Inbound port for the points feature: one user's own points."""

    async def get_points(self, chat_id: int, user_id: int, username: str) -> RankingEntry: ...
