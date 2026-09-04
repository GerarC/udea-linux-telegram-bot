from dataclasses import dataclass

from activity.domain.model.user_activity import UserActivity


@dataclass(frozen=True)
class MonthlyRankingEntry:
    activity: UserActivity
    position: int
    previous_position: int | None
