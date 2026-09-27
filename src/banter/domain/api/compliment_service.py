from typing import Protocol


class ComplimentService(Protocol):
    """Inbound port for the banter feature: compliment (halagar) a target user in a chat."""

    async def compliment(self, chat_id: int, target_user_id: int | None, target_username: str) -> str:
        """Returns the compliment phrase. Records the hit in banter_stats only when target_user_id is known."""
        ...
