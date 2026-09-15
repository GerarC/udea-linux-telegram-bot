from confessions.domain.api.confession_listing_service import ConfessionListingService
from confessions.domain.model.confession import Confession
from confessions.domain.spi.confession_repository_port import ConfessionRepositoryPort
from confessions.domain.utils.constants import RECENT_CONFESSIONS_LIMIT


class ConfessionListingUsecase(ConfessionListingService):
    def __init__(self, repository_port: ConfessionRepositoryPort) -> None:
        self._repository_port = repository_port

    async def list_confessions(self, chat_id: int) -> list[Confession]:
        return await self._repository_port.get_recent_confessions(chat_id, RECENT_CONFESSIONS_LIMIT)
