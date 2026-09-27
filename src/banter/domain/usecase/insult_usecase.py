from banter.domain.api.insult_service import InsultService
from banter.domain.spi.banter_phrase_port import BanterPhrasePort
from banter.domain.spi.banter_stats_port import BanterStatsPort

FALLBACK_INSULT = "no tengo insultos guardados todavía, agrega uno con /agregar_insulto"


class InsultUsecase(InsultService):
    def __init__(self, phrase_port: BanterPhrasePort, stats_port: BanterStatsPort) -> None:
        self._phrase_port = phrase_port
        self._stats_port = stats_port

    async def insult(self, chat_id: int, target_user_id: int | None, target_username: str) -> str:
        phrase = await self._phrase_port.get_random_insult(chat_id)
        if target_user_id is not None:
            await self._stats_port.record_insult(chat_id, target_user_id, target_username)
        return phrase or FALLBACK_INSULT
