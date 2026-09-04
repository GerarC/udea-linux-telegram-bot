from dataclasses import dataclass

from activity.domain.model.user_activity import UserActivity


@dataclass(frozen=True)
class GroupStats:
    messages_this_month: int
    messages_all_time: int
    active_participants_this_month: int
    top_user_this_month: UserActivity | None
    peak_hour: int | None
    peak_weekday: int | None
    extra_lines: list[str]
