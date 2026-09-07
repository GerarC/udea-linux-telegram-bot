from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort
from polls.domain.api.chat_poll_count_service import ChatPollCountService


class PollsGroupStatsProvider(GroupStatsProviderPort):
    """Adapts ChatPollCountService into a GroupStatsProviderPort line for /stats_grupo."""

    def __init__(self, chat_poll_count_service: ChatPollCountService) -> None:
        self._chat_poll_count_service = chat_poll_count_service

    async def get_group_stat_line(self, chat_id: int) -> str | None:
        count = await self._chat_poll_count_service.get_chat_poll_count(chat_id)
        if count == 0:
            return None
        return f"Encuestas creadas: {count}"
