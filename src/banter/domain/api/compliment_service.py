from typing import Protocol


class ComplimentService(Protocol):
    """Inbound port for the banter feature: a random compliment."""

    async def compliment(self) -> str: ...
