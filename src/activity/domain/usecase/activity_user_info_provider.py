from activity.domain.api.all_time_stats_service import AllTimeStatsService
from activity.domain.api.monthly_stats_service import MonthlyStatsService
from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort


class ActivityUserInfoProvider(UserInfoProviderPort):
    """Adapts MonthlyStatsService + AllTimeStatsService into a UserInfoProviderPort section for /usuario_info."""

    def __init__(self, monthly_stats_service: MonthlyStatsService, all_time_stats_service: AllTimeStatsService) -> None:
        self._monthly_stats_service = monthly_stats_service
        self._all_time_stats_service = all_time_stats_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        monthly = await self._monthly_stats_service.get_monthly_stats(chat_id, user_id)
        all_time = await self._all_time_stats_service.get_all_time_stats(chat_id, user_id)
        if monthly is None and all_time is None:
            return None

        lines = []
        if monthly is not None:
            count, position = monthly
            lines.append(f"Mensajes este mes: {count} (posición #{position})")
        else:
            lines.append("Mensajes este mes: 0")

        if all_time is not None:
            count, position = all_time
            lines.append(f"Mensajes en total: {count} (posición #{position})")

        return UserInfoSection(title="📢 Actividad", lines=lines)
