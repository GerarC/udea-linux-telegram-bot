from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort
from polls.domain.api.poll_service import PollService


class PollsUserInfoProvider(UserInfoProviderPort):
    """Adapts PollService into a UserInfoProviderPort section for /usuario_info."""

    def __init__(self, poll_service: PollService) -> None:
        self._poll_service = poll_service

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        count = await self._poll_service.get_poll_count(chat_id, user_id)
        if count == 0:
            return None
        return UserInfoSection(title="🗳️ Encuestas", lines=[f"Encuestas creadas: {count}"])
