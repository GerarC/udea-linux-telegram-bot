from banter.domain.spi.banter_phrase_port import BanterPhrasePort

FALLBACK_INSULT = "no tengo insultos guardados todavía, agrega algunos en banter_insults"
FALLBACK_COMPLIMENT = "no tengo cumplidos guardados todavía, agrega algunos en banter_compliments"


class BanterUsecase:
    def __init__(self, phrase_port: BanterPhrasePort) -> None:
        self._phrase_port = phrase_port

    async def insult(self) -> str:
        phrase = await self._phrase_port.get_random_insult()
        return phrase or FALLBACK_INSULT

    async def compliment(self) -> str:
        phrase = await self._phrase_port.get_random_compliment()
        return phrase or FALLBACK_COMPLIMENT
