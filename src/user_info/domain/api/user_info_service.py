from typing import Protocol

from user_info.domain.model.user_info import UserInfo


class UserInfoService(Protocol):
    """Inbound port: aggregates the /usuario_info sections contributed by every feature."""

    async def get_user_info(self, chat_id: int, user_id: int, username: str) -> UserInfo: ...
