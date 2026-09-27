from news.domain.model.news_item import NewsItem
from news.domain.usecase.news_usecase import NewsUsecase
from news.domain.utils.constants import TRIGGER_PATTERN
from tests.news.fakes import FakeNewsFeedPort, FakeNewsHistoryPort


def _make_usecase(feed_port: FakeNewsFeedPort, history_port: FakeNewsHistoryPort) -> NewsUsecase:
    return NewsUsecase(feed_port=feed_port, history_port=history_port, trigger_pattern=TRIGGER_PATTERN)


async def test_returns_none_and_skips_ports_when_text_does_not_trigger():
    history_port = FakeNewsHistoryPort()
    usecase = _make_usecase(FakeNewsFeedPort(), history_port)

    result = await usecase.handle_message(chat_id=1, text="hola como estas")

    assert result is None
    assert history_port.try_fire_calls == []


async def test_returns_none_when_cooldown_is_active():
    history_port = FakeNewsHistoryPort(can_fire=False)
    usecase = _make_usecase(FakeNewsFeedPort([NewsItem(title="x", link="l", source="s")]), history_port)

    result = await usecase.handle_message(chat_id=1, text="hablemos de tecnología")

    assert result is None


async def test_returns_none_when_feed_is_empty():
    usecase = _make_usecase(FakeNewsFeedPort([]), FakeNewsHistoryPort(can_fire=True))

    result = await usecase.handle_message(chat_id=1, text="tecnología")

    assert result is None


async def test_fires_and_marks_sent_when_triggered_and_not_on_cooldown():
    item = NewsItem(title="x", link="link-1", source="s")
    history_port = FakeNewsHistoryPort(can_fire=True)
    usecase = _make_usecase(FakeNewsFeedPort([item]), history_port)

    result = await usecase.handle_message(chat_id=1, text="hablemos de linux")

    assert result == item
    assert history_port.try_fire_calls == [1]
    assert history_port.marked == [(1, "link-1")]


async def test_avoids_already_seen_items_when_picking():
    seen_item = NewsItem(title="seen", link="seen-link", source="s")
    fresh_item = NewsItem(title="fresh", link="fresh-link", source="s")
    history_port = FakeNewsHistoryPort(can_fire=True, recent=["seen-link"])
    usecase = _make_usecase(FakeNewsFeedPort([seen_item, fresh_item]), history_port)

    result = await usecase.handle_message(chat_id=1, text="tecnología")

    assert result == fresh_item
    assert history_port.marked == [(1, "fresh-link")]


async def test_falls_back_to_any_item_when_everything_was_already_seen():
    item = NewsItem(title="x", link="link-1", source="s")
    history_port = FakeNewsHistoryPort(can_fire=True, recent=["link-1"])
    usecase = _make_usecase(FakeNewsFeedPort([item]), history_port)

    result = await usecase.handle_message(chat_id=1, text="tecnología")

    assert result == item
