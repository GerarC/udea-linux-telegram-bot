from datetime import date, datetime
from zoneinfo import ZoneInfo


def now_in(zone: ZoneInfo) -> datetime:
    return datetime.now(zone)


def current_month(zone: ZoneInfo) -> date:
    now = now_in(zone)
    return date(now.year, now.month, 1)


def previous_month(period_month: date) -> date:
    if period_month.month == 1:
        return date(period_month.year - 1, 12, 1)
    return date(period_month.year, period_month.month - 1, 1)


def months_back(period_month: date, n: int) -> date:
    month_index = period_month.year * 12 + (period_month.month - 1) - n
    return date(month_index // 12, month_index % 12 + 1, 1)
