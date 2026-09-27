from banter.domain.api.add_insult_service import AddInsultService
from banter.domain.spi.banter_phrase_port import BanterPhrasePort


class AddInsultUsecase(AddInsultService):
    def __init__(self, phrase_port: BanterPhrasePort) -> None:
        self._phrase_port = phrase_port

    async def add(self, chat_id: int, requester_is_admin: bool, phrase: str) -> bool:
        if not requester_is_admin:
            return False

        await self._phrase_port.add_insult(chat_id, phrase)
        return True
