from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MonthlyActivity:
    period_month: date
    message_count: int
