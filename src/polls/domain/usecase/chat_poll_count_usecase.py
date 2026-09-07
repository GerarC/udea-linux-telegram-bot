from polls.domain.api.chat_poll_count_service import ChatPollCountService
from polls.domain.spi.poll_repository_port import PollRepositoryPort


class ChatPollCountUsecase(ChatPollCountService):
    def __init__(self, repository_port: PollRepositoryPort) -> None:
        self._repository_port = repository_port

    async def get_chat_poll_count(self, chat_id: int) -> int:
        return await self._repository_port.get_chat_poll_count(chat_id)
