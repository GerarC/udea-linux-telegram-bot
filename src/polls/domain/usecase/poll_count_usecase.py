from polls.domain.api.poll_count_service import PollCountService
from polls.domain.spi.poll_repository_port import PollRepositoryPort


class PollCountUsecase(PollCountService):
    def __init__(self, repository_port: PollRepositoryPort) -> None:
        self._repository_port = repository_port

    async def get_poll_count(self, chat_id: int, user_id: int) -> int:
        return await self._repository_port.get_poll_count(chat_id, user_id)
