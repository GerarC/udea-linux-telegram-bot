from typing import Protocol


class HoroscopePhrasePort(Protocol):
    """Outbound port for fetching horoscope phrases."""

    async def get_phrase_count(self) -> int: ...

    async def get_phrase(self, index: int) -> str: ...
