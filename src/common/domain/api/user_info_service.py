from typing import Protocol

from common.domain.model.user_info import UserInfo


class UserInfoService(Protocol):
    """Inbound port: aggregates the /info_usuario sections contributed by every feature."""

    async def get_user_info(self, chat_id: int, user_id: int, username: str) -> UserInfo: ...
