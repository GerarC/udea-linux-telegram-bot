from typing import Protocol


class PollRecorderService(Protocol):
    """Inbound port for the polls feature: recording a created poll."""

    async def record_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None: ...
