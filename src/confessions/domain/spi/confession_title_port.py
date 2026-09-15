from typing import Protocol

from confessions.domain.model.confession_title import ConfessionTitle


class ConfessionTitlePort(Protocol):
    """Outbound port for fetching confession flavor titles."""

    async def get_random_title(self) -> ConfessionTitle: ...
