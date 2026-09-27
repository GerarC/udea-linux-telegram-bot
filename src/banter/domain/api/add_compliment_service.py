from typing import Protocol


class AddComplimentService(Protocol):
    """Inbound port for the banter feature: an admin adds a new compliment phrase to their chat."""

    async def add(self, chat_id: int, requester_is_admin: bool, phrase: str) -> bool:
        """Returns False when the requester is not an admin (request denied)."""
        ...
