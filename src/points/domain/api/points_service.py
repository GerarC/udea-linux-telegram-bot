from typing import Protocol

from points.domain.model.grant_result import GrantResult
from points.domain.model.ranking_entry import RankingEntry


class PointsService(Protocol):
    """Inbound port for the points feature."""

    async def grant_points(
        self,
        chat_id: int,
        granter_is_admin: bool,
        target_id: int,
        target_username: str,
        amount: int,
    ) -> GrantResult | None:
        """Returns None when the granter is not an admin (request denied)."""
        ...

    async def get_ranking(self, chat_id: int, limit: int | None = None) -> list[RankingEntry]: ...

    async def get_points(self, chat_id: int, user_id: int, username: str) -> RankingEntry: ...

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        """Returns the user's 1-based rank by points in this chat, or None if they have no row."""
        ...
