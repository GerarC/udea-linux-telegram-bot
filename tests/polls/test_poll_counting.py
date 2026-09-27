from polls.domain.usecase.chat_poll_count_usecase import ChatPollCountUsecase
from polls.domain.usecase.poll_count_usecase import PollCountUsecase
from polls.domain.usecase.poll_recorder_usecase import PollRecorderUsecase
from tests.polls.fakes import FakePollRepository


async def test_recording_a_poll_increases_both_the_user_and_chat_count():
    repo = FakePollRepository()
    recorder = PollRecorderUsecase(repository_port=repo)

    await recorder.record_poll(chat_id=1, user_id=42, username="fulano", question="¿algo?")

    assert repo.saved == [(1, 42, "fulano", "¿algo?")]
    assert await PollCountUsecase(repository_port=repo).get_poll_count(1, 42) == 1
    assert await ChatPollCountUsecase(repository_port=repo).get_chat_poll_count(1) == 1


async def test_counts_are_scoped_per_chat_and_user():
    repo = FakePollRepository()
    recorder = PollRecorderUsecase(repository_port=repo)

    await recorder.record_poll(chat_id=1, user_id=42, username="fulano", question="q1")
    await recorder.record_poll(chat_id=1, user_id=99, username="sutano", question="q2")
    await recorder.record_poll(chat_id=2, user_id=42, username="fulano", question="q3")

    assert await PollCountUsecase(repository_port=repo).get_poll_count(1, 42) == 1
    assert await ChatPollCountUsecase(repository_port=repo).get_chat_poll_count(1) == 2
    assert await ChatPollCountUsecase(repository_port=repo).get_chat_poll_count(2) == 1


async def test_counts_are_zero_when_nothing_recorded():
    repo = FakePollRepository()

    assert await PollCountUsecase(repository_port=repo).get_poll_count(1, 42) == 0
    assert await ChatPollCountUsecase(repository_port=repo).get_chat_poll_count(1) == 0
