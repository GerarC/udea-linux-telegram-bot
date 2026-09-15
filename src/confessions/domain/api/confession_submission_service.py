from typing import Protocol

from confessions.domain.model.confession import Confession


class ConfessionSubmissionService(Protocol):
    """Inbound port for the confessions feature: submitting a new anonymous confession."""

    async def submit_confession(self, chat_id: int, user_id: int, username: str, content: str) -> Confession: ...
