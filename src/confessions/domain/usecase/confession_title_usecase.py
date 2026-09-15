from confessions.domain.api.confession_title_service import ConfessionTitleService
from confessions.domain.model.confession_title import ConfessionTitle
from confessions.domain.spi.confession_title_port import ConfessionTitlePort


class ConfessionTitleUsecase(ConfessionTitleService):
    def __init__(self, title_port: ConfessionTitlePort) -> None:
        self._title_port = title_port

    async def get_random_title(self) -> ConfessionTitle:
        return await self._title_port.get_random_title()
