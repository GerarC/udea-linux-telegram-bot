from typing import Protocol


class InsultService(Protocol):
    """Inbound port for the banter feature: a random insult."""

    async def insult(self) -> str: ...
