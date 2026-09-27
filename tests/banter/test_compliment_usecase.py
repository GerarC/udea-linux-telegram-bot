from banter.domain.usecase.compliment_usecase import FALLBACK_COMPLIMENT, ComplimentUsecase
from tests.banter.fakes import FakeBanterPhrasePort, FakeBanterStatsPort


async def test_compliment_returns_phrase_and_records_stats_when_target_known():
    phrase_port = FakeBanterPhrasePort(compliments={1: ["te ves bien hoy"]})
    stats_port = FakeBanterStatsPort()
    usecase = ComplimentUsecase(phrase_port=phrase_port, stats_port=stats_port)

    result = await usecase.compliment(chat_id=1, target_user_id=42, target_username="fulano")

    assert result == "te ves bien hoy"
    stats = await stats_port.get_stats(1, 42)
    assert stats.compliments_received == 1
    assert stats.insults_received == 0


async def test_compliment_does_not_record_stats_when_target_unknown():
    phrase_port = FakeBanterPhrasePort(compliments={1: ["te ves bien hoy"]})
    stats_port = FakeBanterStatsPort()
    usecase = ComplimentUsecase(phrase_port=phrase_port, stats_port=stats_port)

    result = await usecase.compliment(chat_id=1, target_user_id=None, target_username="texto libre")

    assert result == "te ves bien hoy"
    assert stats_port.stats == {}


async def test_compliment_falls_back_when_chat_has_no_phrases():
    usecase = ComplimentUsecase(phrase_port=FakeBanterPhrasePort(), stats_port=FakeBanterStatsPort())

    result = await usecase.compliment(chat_id=1, target_user_id=None, target_username="x")

    assert result == FALLBACK_COMPLIMENT
