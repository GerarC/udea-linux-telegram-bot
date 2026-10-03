from datetime import UTC, datetime

from confessions.domain.model.confession import Confession
from confessions.domain.spi.confession_repository_port import ConfessionRepositoryPort


class FakeConfessionRepository(ConfessionRepositoryPort):
    def __init__(self) -> None:
        self.confessions: dict[int, Confession] = {}
        self._next_id = 1

    async def create_confession(
        self, chat_id: int, user_id: int, username: str, full_name: str, content: str
    ) -> Confession:
        confession = Confession(
            id=self._next_id,
            chat_id=chat_id,
            user_id=user_id,
            content=content,
            created_at=datetime.now(UTC),
            is_deleted=False,
        )
        self.confessions[confession.id] = confession
        self._next_id += 1
        return confession

    async def get_recent_confessions(self, chat_id: int, limit: int) -> list[Confession]:
        matching = [c for c in self.confessions.values() if c.chat_id == chat_id and not c.is_deleted]
        matching.sort(key=lambda c: c.created_at, reverse=True)
        return matching[:limit]

    async def soft_delete_confession(self, chat_id: int, confession_id: int) -> Confession | None:
        confession = self.confessions.get(confession_id)
        if confession is None or confession.chat_id != chat_id or confession.is_deleted:
            return None
        confession.is_deleted = True
        return confession
