from typing import Protocol


class UsernameResolverService(Protocol):
    """Inbound port: resolves a typed @username into a user_id, raising UserNotFoundError if unknown."""

    async def resolve_username(self, chat_id: int, username: str) -> int: ...
