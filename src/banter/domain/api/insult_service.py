from typing import Protocol


class InsultService(Protocol):
    """Inbound port for the banter feature: insult a target user in a chat."""

    async def insult(
        self, chat_id: int, target_user_id: int | None, target_username: str, target_full_name: str
    ) -> str:
        """Returns the insult phrase. Records the hit in banter_stats only when target_user_id is known."""
        ...
