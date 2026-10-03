from common.domain.model.group_stat_line import GroupStatLine
from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort
from polls.domain.api.chat_poll_count_service import ChatPollCountService


class PollsGroupStatsProvider(GroupStatsProviderPort):
    """Adapts ChatPollCountService into GroupStatsProviderPort lines for /stats_grupo."""

    def __init__(self, chat_poll_count_service: ChatPollCountService) -> None:
        self._chat_poll_count_service = chat_poll_count_service

    async def get_group_stat_lines(self, chat_id: int) -> list[GroupStatLine]:
        count = await self._chat_poll_count_service.get_chat_poll_count(chat_id)
        if count == 0:
            return []
        return [GroupStatLine(label="Encuestas creadas", value=str(count))]
