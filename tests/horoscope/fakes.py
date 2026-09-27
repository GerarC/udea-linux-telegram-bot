from horoscope.domain.spi.horoscope_phrase_port import HoroscopePhrasePort


class FakeHoroscopePhrasePort(HoroscopePhrasePort):
    def __init__(self, phrases: list[str] | None = None) -> None:
        self.phrases = list(phrases or [])

    async def get_phrase_count(self) -> int:
        return len(self.phrases)

    async def get_phrase(self, index: int) -> str:
        return self.phrases[index]
