from typing import Protocol

from confessions.domain.model.confession import Confession


class ConfessionRepositoryPort(Protocol):
    """Outbound port for persisting and querying confessions."""

    async def create_confession(self, chat_id: int, user_id: int, username: str, content: str) -> Confession: ...

    async def get_recent_confessions(self, chat_id: int, limit: int) -> list[Confession]: ...

    async def soft_delete_confession(self, chat_id: int, confession_id: int) -> Confession | None: ...
