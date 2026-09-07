from typing import Protocol


class ActivityService(Protocol):
    """Inbound port for the activity feature: recording activity (command)."""

    async def register_message(self, chat_id: int, user_id: int, username: str) -> None: ...
