from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort
from polls.domain.api.poll_service import PollService


class PollsGroupStatsProvider(GroupStatsProviderPort):
    """Adapts PollService into a GroupStatsProviderPort line for /stats_grupo."""

    def __init__(self, poll_service: PollService) -> None:
        self._poll_service = poll_service

    async def get_group_stat_line(self, chat_id: int) -> str | None:
        count = await self._poll_service.get_chat_poll_count(chat_id)
        if count == 0:
            return None
        return f"Encuestas creadas: {count}"
