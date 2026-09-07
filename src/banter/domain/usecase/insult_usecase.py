from banter.domain.api.insult_service import InsultService
from banter.domain.spi.banter_phrase_port import BanterPhrasePort

FALLBACK_INSULT = "no tengo insultos guardados todavía, agrega algunos en banter_insults"


class InsultUsecase(InsultService):
    def __init__(self, phrase_port: BanterPhrasePort) -> None:
        self._phrase_port = phrase_port

    async def insult(self) -> str:
        phrase = await self._phrase_port.get_random_insult()
        return phrase or FALLBACK_INSULT
