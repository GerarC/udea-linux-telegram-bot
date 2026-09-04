from activity.domain.api.activity_service import ActivityService
from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort


class ActivityUserInfoProvider(UserInfoProviderPort):
    """Adapts ActivityService into a UserInfoProviderPort section for /info_usuario."""

    def __init__(self, activity_service: ActivityService) -> None:
        self._activity_service = activity_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        monthly = await self._activity_service.get_monthly_stats(chat_id, user_id)
        all_time = await self._activity_service.get_all_time_stats(chat_id, user_id)
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
