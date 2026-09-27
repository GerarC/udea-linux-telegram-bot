from typing import Protocol


class TargetResolverService(Protocol):
    """Inbound port for the banter feature: resolves a typed @username to a user_id."""

    async def resolve(self, chat_id: int, username: str) -> int | None:
        """Returns None when the bot hasn't seen this username post in this chat yet."""
        ...
