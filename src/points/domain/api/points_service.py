from typing import Protocol

from points.domain.model.grant_result import GrantResult


class PointsService(Protocol):
    """Inbound port for the points feature: granting/removing points."""

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
