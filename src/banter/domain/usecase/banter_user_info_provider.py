from banter.domain.api.user_banter_stats_service import UserBanterStatsService
from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort


class BanterUserInfoProvider(UserInfoProviderPort):
    """Adapts UserBanterStatsService into a UserInfoProviderPort section for /gdb."""

    def __init__(self, user_banter_stats_service: UserBanterStatsService) -> None:
        self._user_banter_stats_service = user_banter_stats_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        stats = await self._user_banter_stats_service.get_stats(chat_id, user_id)
        if stats is None:
            return None

        lines = [
            f"Veces insultado: {stats.insults_received}",
            f"Veces halagado: {stats.compliments_received}",
        ]
        return UserInfoSection(title="😈 Banter", lines=lines)
