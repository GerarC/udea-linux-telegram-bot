from confessions.domain.api.confession_submission_service import ConfessionSubmissionService
from confessions.domain.error.confession_too_long_error import ConfessionTooLongError
from confessions.domain.error.confession_too_short_error import ConfessionTooShortError
from confessions.domain.model.confession import Confession
from confessions.domain.spi.confession_repository_port import ConfessionRepositoryPort
from confessions.domain.utils.constants import MAX_CONTENT_LENGTH, MIN_CONTENT_LENGTH


class ConfessionSubmissionUsecase(ConfessionSubmissionService):
    def __init__(self, repository_port: ConfessionRepositoryPort) -> None:
        self._repository_port = repository_port

    async def submit_confession(self, chat_id: int, user_id: int, username: str, content: str) -> Confession:
        normalized = content.strip()
        if len(normalized) < MIN_CONTENT_LENGTH:
            raise ConfessionTooShortError()
        if len(normalized) > MAX_CONTENT_LENGTH:
            raise ConfessionTooLongError()

        return await self._repository_port.create_confession(chat_id, user_id, username, normalized)
