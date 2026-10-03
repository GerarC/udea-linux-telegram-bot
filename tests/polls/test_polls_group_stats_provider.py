from common.domain.model.group_stat_line import GroupStatLine
from polls.domain.usecase.chat_poll_count_usecase import ChatPollCountUsecase
from polls.domain.usecase.poll_recorder_usecase import PollRecorderUsecase
from polls.domain.usecase.polls_group_stats_provider import PollsGroupStatsProvider
from tests.polls.fakes import FakePollRepository


async def test_lines_are_empty_when_chat_has_no_polls():
    repo = FakePollRepository()
    provider = PollsGroupStatsProvider(chat_poll_count_service=ChatPollCountUsecase(repository_port=repo))

    assert await provider.get_group_stat_lines(chat_id=1) == []


async def test_lines_report_the_chat_poll_count():
    repo = FakePollRepository()
    await PollRecorderUsecase(repository_port=repo).record_poll(1, 42, "fulano", "fulano", "q")
    provider = PollsGroupStatsProvider(chat_poll_count_service=ChatPollCountUsecase(repository_port=repo))

    assert await provider.get_group_stat_lines(chat_id=1) == [GroupStatLine("Encuestas creadas", "1")]
