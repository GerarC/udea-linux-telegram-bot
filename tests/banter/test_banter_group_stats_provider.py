from banter.domain.usecase.banter_group_stats_provider import BanterGroupStatsProvider
from banter.domain.usecase.top_banter_stats_usecase import TopBanterStatsUsecase
from common.domain.model.group_stat_line import GroupStatLine, GroupStatMention
from tests.banter.fakes import FakeBanterStatsPort


async def test_lines_are_empty_when_chat_has_no_data():
    provider = BanterGroupStatsProvider(TopBanterStatsUsecase(FakeBanterStatsPort()))

    assert await provider.get_group_stat_lines(chat_id=1) == []


async def test_lines_report_most_insulted_and_most_complimented():
    stats_port = FakeBanterStatsPort()
    await stats_port.record_insult(1, 42, "fulano", "fulano")
    await stats_port.record_insult(1, 42, "fulano", "fulano")
    await stats_port.record_compliment(1, 7, "sutano", "sutano")
    provider = BanterGroupStatsProvider(TopBanterStatsUsecase(stats_port))

    lines = await provider.get_group_stat_lines(chat_id=1)

    assert lines == [
        GroupStatLine("Más insultado", "(2 veces)", GroupStatMention(42, "fulano", "fulano")),
        GroupStatLine("Más halagado", "(1 veces)", GroupStatMention(7, "sutano", "sutano")),
    ]


async def test_lines_only_report_the_side_with_data():
    stats_port = FakeBanterStatsPort()
    await stats_port.record_insult(1, 42, "fulano", "fulano")
    provider = BanterGroupStatsProvider(TopBanterStatsUsecase(stats_port))

    lines = await provider.get_group_stat_lines(chat_id=1)

    assert lines == [GroupStatLine("Más insultado", "(1 veces)", GroupStatMention(42, "fulano", "fulano"))]
