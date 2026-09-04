from typing import Protocol


class BanterService(Protocol):
    """Inbound port for the banter feature."""

    async def insult(self) -> str: ...

    async def compliment(self) -> str: ...
