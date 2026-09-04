import os
from dataclasses import dataclass

from points.domain.utils.constants import DEFAULT_RANKING_LIMIT


@dataclass(frozen=True)
class PointsSettings:
    ranking_limit: int


def load_points_settings() -> PointsSettings:
    ranking_limit = int(os.environ.get("POINTS_RANKING_LIMIT", DEFAULT_RANKING_LIMIT))
    return PointsSettings(ranking_limit=ranking_limit)
