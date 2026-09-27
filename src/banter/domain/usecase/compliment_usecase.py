from banter.domain.api.compliment_service import ComplimentService
from banter.domain.spi.banter_phrase_port import BanterPhrasePort
from banter.domain.spi.banter_stats_port import BanterStatsPort

FALLBACK_COMPLIMENT = "no tengo halagos guardados todavía, agrega uno con /agregar_halago"


class ComplimentUsecase(ComplimentService):
    def __init__(self, phrase_port: BanterPhrasePort, stats_port: BanterStatsPort) -> None:
        self._phrase_port = phrase_port
        self._stats_port = stats_port

    async def compliment(self, chat_id: int, target_user_id: int | None, target_username: str) -> str:
        phrase = await self._phrase_port.get_random_compliment(chat_id)
        if target_user_id is not None:
            await self._stats_port.record_compliment(chat_id, target_user_id, target_username)
        return phrase or FALLBACK_COMPLIMENT
