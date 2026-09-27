from datetime import date

from activity.domain.utils.clock import months_back, previous_month


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
