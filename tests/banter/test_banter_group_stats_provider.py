from banter.domain.usecase.banter_group_stats_provider import BanterGroupStatsProvider
from banter.domain.usecase.top_banter_stats_usecase import TopBanterStatsUsecase
from tests.banter.fakes import FakeBanterStatsPort


async def test_line_is_none_when_chat_has_no_data():
    provider = BanterGroupStatsProvider(TopBanterStatsUsecase(FakeBanterStatsPort()))

    assert await provider.get_group_stat_line(chat_id=1) is None


async def test_line_reports_most_insulted_and_most_complimented():
    stats_port = FakeBanterStatsPort()
    await stats_port.record_insult(1, 42, "fulano")
    await stats_port.record_insult(1, 42, "fulano")
    await stats_port.record_compliment(1, 7, "sutano")
    provider = BanterGroupStatsProvider(TopBanterStatsUsecase(stats_port))

    line = await provider.get_group_stat_line(chat_id=1)

    assert line == "Más insultado: @fulano (2 veces)\nMás halagado: @sutano (1 veces)"


async def test_line_only_reports_the_side_with_data():
    stats_port = FakeBanterStatsPort()
    await stats_port.record_insult(1, 42, "fulano")
    provider = BanterGroupStatsProvider(TopBanterStatsUsecase(stats_port))

    line = await provider.get_group_stat_line(chat_id=1)

    assert line == "Más insultado: @fulano (1 veces)"
