from polls.domain.api.poll_recorder_service import PollRecorderService
from polls.domain.spi.poll_repository_port import PollRepositoryPort


class PollRecorderUsecase(PollRecorderService):
    def __init__(self, repository_port: PollRepositoryPort) -> None:
        self._repository_port = repository_port

    async def record_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None:
        await self._repository_port.save_poll(chat_id, user_id, username, question)
