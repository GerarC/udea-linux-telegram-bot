from banter.domain.api.compliment_service import ComplimentService
from banter.domain.spi.banter_phrase_port import BanterPhrasePort

FALLBACK_COMPLIMENT = "no tengo cumplidos guardados todavía, agrega algunos en banter_compliments"


class ComplimentUsecase(ComplimentService):
    def __init__(self, phrase_port: BanterPhrasePort) -> None:
        self._phrase_port = phrase_port

    async def compliment(self) -> str:
        phrase = await self._phrase_port.get_random_compliment()
        return phrase or FALLBACK_COMPLIMENT
