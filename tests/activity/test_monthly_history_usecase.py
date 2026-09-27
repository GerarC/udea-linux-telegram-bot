from datetime import date

import activity.domain.usecase.monthly_history_usecase as monthly_history_usecase_module
from activity.domain.model.monthly_activity import MonthlyActivity
from activity.domain.usecase.monthly_history_usecase import MonthlyHistoryUsecase
from tests.activity.fakes import FakeActivityRepository


async def test_fills_gaps_and_windows_to_the_last_six_months(monkeypatch):
    monkeypatch.setattr(monthly_history_usecase_module, "current_month", lambda zone: date(2026, 9, 1))
    repo = FakeActivityRepository(
        monthly_history=[
            MonthlyActivity(period_month=date(2026, 3, 1), message_count=999),  # outside the 6-month window
            MonthlyActivity(period_month=date(2026, 7, 1), message_count=100),
            MonthlyActivity(period_month=date(2026, 9, 1), message_count=50),
        ]
    )
    usecase = MonthlyHistoryUsecase(repository_port=repo)

    history = await usecase.get_monthly_history(chat_id=1)

    assert [entry.period_month for entry in history] == [
        date(2026, 4, 1),
        date(2026, 5, 1),
        date(2026, 6, 1),
        date(2026, 7, 1),
        date(2026, 8, 1),
        date(2026, 9, 1),
    ]
    assert [entry.message_count for entry in history] == [0, 0, 0, 100, 0, 50]


async def test_returns_all_zeros_when_chat_has_no_history(monkeypatch):
    monkeypatch.setattr(monthly_history_usecase_module, "current_month", lambda zone: date(2026, 1, 1))
    usecase = MonthlyHistoryUsecase(repository_port=FakeActivityRepository())

    history = await usecase.get_monthly_history(chat_id=1)

    assert len(history) == 6
    assert all(entry.message_count == 0 for entry in history)
