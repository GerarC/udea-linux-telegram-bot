from banter.domain.usecase.banter_user_info_provider import BanterUserInfoProvider
from banter.domain.usecase.user_banter_stats_usecase import UserBanterStatsUsecase
from tests.banter.fakes import FakeBanterStatsPort


async def test_section_is_none_when_user_has_no_stats():
    provider = BanterUserInfoProvider(UserBanterStatsUsecase(FakeBanterStatsPort()))

    assert await provider.get_section(chat_id=1, user_id=42, username="fulano", full_name="fulano") is None


async def test_section_reports_both_counters():
    stats_port = FakeBanterStatsPort()
    await stats_port.record_insult(1, 42, "fulano", "fulano")
    await stats_port.record_compliment(1, 42, "fulano", "fulano")
    provider = BanterUserInfoProvider(UserBanterStatsUsecase(stats_port))

    section = await provider.get_section(chat_id=1, user_id=42, username="fulano", full_name="fulano")

    assert section.title == "😈 Banter"
    assert section.lines == ["Veces insultado: 1", "Veces halagado: 1"]
