from polls.domain.usecase.poll_count_usecase import PollCountUsecase
from polls.domain.usecase.poll_recorder_usecase import PollRecorderUsecase
from polls.domain.usecase.polls_user_info_provider import PollsUserInfoProvider
from tests.polls.fakes import FakePollRepository


async def test_section_is_none_when_user_has_no_polls():
    repo = FakePollRepository()
    provider = PollsUserInfoProvider(poll_count_service=PollCountUsecase(repository_port=repo))

    assert await provider.get_section(chat_id=1, user_id=42, username="fulano") is None


async def test_section_reports_the_poll_count():
    repo = FakePollRepository()
    await PollRecorderUsecase(repository_port=repo).record_poll(1, 42, "fulano", "q")
    provider = PollsUserInfoProvider(poll_count_service=PollCountUsecase(repository_port=repo))

    section = await provider.get_section(chat_id=1, user_id=42, username="fulano")

    assert section.title == "🗳️ Encuestas"
    assert section.lines == ["Encuestas creadas: 1"]
