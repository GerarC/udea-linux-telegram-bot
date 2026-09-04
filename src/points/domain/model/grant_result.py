from dataclasses import dataclass

from points.domain.model.ranking_entry import RankingEntry
from points.domain.model.user_points import UserPoints


@dataclass(frozen=True)
class GrantResult:
    target: UserPoints
    level_label: str
    ranking: list[RankingEntry]
