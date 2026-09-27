from banter.domain.usecase.add_insult_usecase import AddInsultUsecase
from tests.banter.fakes import FakeBanterPhrasePort


async def test_add_insult_rejected_when_not_admin():
    phrase_port = FakeBanterPhrasePort()
    usecase = AddInsultUsecase(phrase_port=phrase_port)

    added = await usecase.add(chat_id=1, requester_is_admin=False, phrase="nuevo insulto")

    assert added is False
    assert phrase_port.added_insults == []


async def test_add_insult_accepted_when_admin():
    phrase_port = FakeBanterPhrasePort()
    usecase = AddInsultUsecase(phrase_port=phrase_port)

    added = await usecase.add(chat_id=1, requester_is_admin=True, phrase="nuevo insulto")

    assert added is True
    assert phrase_port.added_insults == [(1, "nuevo insulto")]
    assert await phrase_port.get_random_insult(1) == "nuevo insulto"
