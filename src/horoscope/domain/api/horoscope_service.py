from typing import Protocol

from horoscope.domain.model.horoscope_reading import HoroscopeReading


class HoroscopeService(Protocol):
    """Inbound port for the horoscope feature: today's deterministic reading for a sign."""

    async def get_horoscope(self, sign: str) -> HoroscopeReading: ...
