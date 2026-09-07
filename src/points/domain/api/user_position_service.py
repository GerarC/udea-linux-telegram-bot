from typing import Protocol


class UserPositionService(Protocol):
    """Inbound port for the points feature: one user's rank in the chat."""

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        """Returns the user's 1-based rank by points in this chat, or None if they have no row."""
        ...
