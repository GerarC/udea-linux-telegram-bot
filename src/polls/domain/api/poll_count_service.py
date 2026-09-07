from typing import Protocol


class PollCountService(Protocol):
    """Inbound port for the polls feature: how many polls one user has created."""

    async def get_poll_count(self, chat_id: int, user_id: int) -> int: ...
