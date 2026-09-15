from typing import Protocol


class MemberLookupPort(Protocol):
    """Outbound port for resolving a typed @username to a user_id within a chat."""

    async def find_user_id_by_username(self, chat_id: int, username: str) -> int | None: ...
