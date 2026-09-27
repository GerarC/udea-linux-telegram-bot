from datetime import date
from zoneinfo import ZoneInfo

from activity.domain.utils.clock import current_month, months_back, now_in, previous_month


def test_now_in_returns_a_timezone_aware_datetime():
    zone = ZoneInfo("America/Bogota")

    now = now_in(zone)

    assert now.tzinfo is not None


def test_current_month_is_the_first_of_the_current_calendar_month():
    zone = ZoneInfo("America/Bogota")

    result = current_month(zone)

    assert result == now_in(zone).date().replace(day=1)


def test_previous_month_rolls_back_a_year_in_january():
    assert previous_month(date(2026, 1, 1)) == date(2025, 12, 1)


def test_months_back_zero_returns_same_month():
    assert months_back(date(2026, 9, 1), 0) == date(2026, 9, 1)


def test_months_back_within_same_year():
    assert months_back(date(2026, 9, 1), 3) == date(2026, 6, 1)


def test_months_back_across_year_boundary():
    assert months_back(date(2026, 2, 1), 3) == date(2025, 11, 1)


def test_months_back_matches_repeated_previous_month():
    start = date(2026, 9, 1)
    expected = start
    for _ in range(5):
        expected = previous_month(expected)

    assert months_back(start, 5) == expected
