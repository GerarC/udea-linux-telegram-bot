from typing import Protocol


class PollRepositoryPort(Protocol):
    """Outbound port: persists and reads per-chat, per-user poll history."""

    async def save_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None: ...

    async def get_poll_count(self, chat_id: int, user_id: int) -> int: ...

    async def get_chat_poll_count(self, chat_id: int) -> int: ...
