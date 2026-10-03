from banter.domain.usecase.insult_usecase import FALLBACK_INSULT, InsultUsecase
from tests.banter.fakes import FakeBanterPhrasePort, FakeBanterStatsPort


async def test_insult_returns_phrase_and_records_stats_when_target_known():
    phrase_port = FakeBanterPhrasePort(insults={1: ["cállate"]})
    stats_port = FakeBanterStatsPort()
    usecase = InsultUsecase(phrase_port=phrase_port, stats_port=stats_port)

    result = await usecase.insult(chat_id=1, target_user_id=42, target_username="fulano", target_full_name="fulano")

    assert result == "cállate"
    stats = await stats_port.get_stats(1, 42)
    assert stats.insults_received == 1
    assert stats.compliments_received == 0


async def test_insult_does_not_record_stats_when_target_unknown():
    phrase_port = FakeBanterPhrasePort(insults={1: ["cállate"]})
    stats_port = FakeBanterStatsPort()
    usecase = InsultUsecase(phrase_port=phrase_port, stats_port=stats_port)

    result = await usecase.insult(
        chat_id=1, target_user_id=None, target_username="texto libre", target_full_name="texto libre"
    )

    assert result == "cállate"
    assert stats_port.stats == {}


async def test_insult_falls_back_when_chat_has_no_phrases():
    usecase = InsultUsecase(phrase_port=FakeBanterPhrasePort(), stats_port=FakeBanterStatsPort())

    result = await usecase.insult(chat_id=1, target_user_id=None, target_username="x", target_full_name="x")

    assert result == FALLBACK_INSULT


async def test_insult_only_uses_phrases_from_its_own_chat():
    phrase_port = FakeBanterPhrasePort(insults={1: ["insulto de chat 1"], 2: ["insulto de chat 2"]})
    usecase = InsultUsecase(phrase_port=phrase_port, stats_port=FakeBanterStatsPort())

    assert (
        await usecase.insult(chat_id=1, target_user_id=None, target_username="x", target_full_name="x")
        == "insulto de chat 1"
    )
    assert (
        await usecase.insult(chat_id=2, target_user_id=None, target_username="x", target_full_name="x")
        == "insulto de chat 2"
    )
