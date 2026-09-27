from banter.domain.usecase.add_compliment_usecase import AddComplimentUsecase
from tests.banter.fakes import FakeBanterPhrasePort


async def test_add_compliment_rejected_when_not_admin():
    phrase_port = FakeBanterPhrasePort()
    usecase = AddComplimentUsecase(phrase_port=phrase_port)

    added = await usecase.add(chat_id=1, requester_is_admin=False, phrase="nuevo halago")

    assert added is False
    assert phrase_port.added_compliments == []


async def test_add_compliment_accepted_when_admin():
    phrase_port = FakeBanterPhrasePort()
    usecase = AddComplimentUsecase(phrase_port=phrase_port)

    added = await usecase.add(chat_id=1, requester_is_admin=True, phrase="nuevo halago")

    assert added is True
    assert phrase_port.added_compliments == [(1, "nuevo halago")]
    assert await phrase_port.get_random_compliment(1) == "nuevo halago"
