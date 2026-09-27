from banter.domain.api.add_compliment_service import AddComplimentService
from banter.domain.spi.banter_phrase_port import BanterPhrasePort


class AddComplimentUsecase(AddComplimentService):
    def __init__(self, phrase_port: BanterPhrasePort) -> None:
        self._phrase_port = phrase_port

    async def add(self, chat_id: int, requester_is_admin: bool, phrase: str) -> bool:
        if not requester_is_admin:
            return False

        await self._phrase_port.add_compliment(chat_id, phrase)
        return True
