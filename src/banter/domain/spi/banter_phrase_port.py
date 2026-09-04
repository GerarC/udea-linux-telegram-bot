from typing import Protocol


class BanterPhrasePort(Protocol):
    """Outbound port for fetching banter phrases."""

    async def get_random_insult(self) -> str: ...

    async def get_random_compliment(self) -> str: ...
