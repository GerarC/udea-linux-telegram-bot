from typing import Protocol

from points.domain.model.user_points import UserPoints


class PointsRepositoryPort(Protocol):
    """Outbound port: persists and reads per-chat, per-user points."""

    async def add_points(self, chat_id: int, user_id: int, username: str, amount: int) -> UserPoints: ...

    async def get_points(self, chat_id: int, user_id: int) -> UserPoints | None: ...

    async def get_ranking(self, chat_id: int, limit: int) -> list[UserPoints]: ...

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        """Returns the user's 1-based rank by points in this chat, or None if they have no row."""
        ...
