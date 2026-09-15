from confessions.domain.api.confession_deletion_service import ConfessionDeletionService
from confessions.domain.error.confession_not_found_error import ConfessionNotFoundError
from confessions.domain.model.confession import Confession
from confessions.domain.spi.confession_repository_port import ConfessionRepositoryPort


class ConfessionDeletionUsecase(ConfessionDeletionService):
    def __init__(self, repository_port: ConfessionRepositoryPort) -> None:
        self._repository_port = repository_port

    async def delete_confession(
        self, chat_id: int, confession_id: int, requester_is_admin: bool
    ) -> Confession | None:
        if not requester_is_admin:
            return None

        confession = await self._repository_port.soft_delete_confession(chat_id, confession_id)
        if confession is None:
            raise ConfessionNotFoundError(confession_id)
        return confession
