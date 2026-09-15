from typing import Protocol

from confessions.domain.model.confession import Confession


class ConfessionListingService(Protocol):
    """Inbound port for the confessions feature: the most recent confessions of a chat."""

    async def list_confessions(self, chat_id: int) -> list[Confession]: ...
