from typing import Protocol


class ChatPollCountService(Protocol):
    """Inbound port for the polls feature: how many polls have been created in a chat."""

    async def get_chat_poll_count(self, chat_id: int) -> int: ...
