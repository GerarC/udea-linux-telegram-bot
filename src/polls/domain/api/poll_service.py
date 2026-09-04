from typing import Protocol

from polls.domain.model.poll import Poll


class PollService(Protocol):
    """Inbound port for the polls feature."""

    def parse_poll(self, raw_text: str) -> Poll:
        """Parses '<question> | <option1> | <option2> [| ...]', raising PollValidationError if invalid."""
        ...

    async def record_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None: ...

    async def get_poll_count(self, chat_id: int, user_id: int) -> int: ...

    async def get_chat_poll_count(self, chat_id: int) -> int: ...
