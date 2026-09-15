from typing import Protocol

from confessions.domain.model.confession_title import ConfessionTitle


class ConfessionTitleService(Protocol):
    async def get_random_title(self) -> ConfessionTitle: ...
