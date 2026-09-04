import asyncio
import logging

from common.domain.model.user_info import UserInfo
from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort


class UserInfoUsecase:
    """Fans out to every registered UserInfoProviderPort and aggregates the sections available.

    A provider failing (e.g. its DB is unreachable) only drops that one section instead
    of failing the whole /info_usuario response - same degrade-gracefully policy as the RSS
    feed adapter uses for individual feeds.
    """

    def __init__(self, providers: list[UserInfoProviderPort]) -> None:
        self._providers = providers

    async def get_user_info(self, chat_id: int, user_id: int, username: str) -> UserInfo:
        results = await asyncio.gather(
            *(self._safe_section(provider, chat_id, user_id, username) for provider in self._providers)
        )
        return UserInfo(user_id=user_id, username=username, sections=[s for s in results if s is not None])

    @staticmethod
    async def _safe_section(
        provider: UserInfoProviderPort, chat_id: int, user_id: int, username: str
    ) -> UserInfoSection | None:
        try:
            return await provider.get_section(chat_id, user_id, username)
        except Exception:
            logging.exception(
                "user_info provider failed",
                extra={"event": "user_info_provider_failed", "provider": type(provider).__name__},
            )
            return None
