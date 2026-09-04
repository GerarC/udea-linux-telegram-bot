from dataclasses import dataclass

from points.domain.model.user_points import UserPoints


@dataclass(frozen=True)
class RankingEntry:
    user_points: UserPoints
    level_label: str
