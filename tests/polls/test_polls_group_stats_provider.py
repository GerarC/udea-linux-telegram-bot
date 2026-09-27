from polls.domain.usecase.chat_poll_count_usecase import ChatPollCountUsecase
from polls.domain.usecase.poll_recorder_usecase import PollRecorderUsecase
from polls.domain.usecase.polls_group_stats_provider import PollsGroupStatsProvider
from tests.polls.fakes import FakePollRepository


async def test_line_is_none_when_chat_has_no_polls():
    repo = FakePollRepository()
    provider = PollsGroupStatsProvider(chat_poll_count_service=ChatPollCountUsecase(repository_port=repo))

    assert await provider.get_group_stat_line(chat_id=1) is None


async def test_line_reports_the_chat_poll_count():
    repo = FakePollRepository()
    await PollRecorderUsecase(repository_port=repo).record_poll(1, 42, "fulano", "q")
    provider = PollsGroupStatsProvider(chat_poll_count_service=ChatPollCountUsecase(repository_port=repo))

    assert await provider.get_group_stat_line(chat_id=1) == "Encuestas creadas: 1"
