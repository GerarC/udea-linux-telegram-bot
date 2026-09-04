import os
from dataclasses import dataclass

from activity.domain.utils.constants import DEFAULT_RANKING_LIMIT, DEFAULT_TIMEZONE


@dataclass(frozen=True)
class ActivitySettings:
    ranking_limit: int
    timezone: str


def load_activity_settings() -> ActivitySettings:
    ranking_limit = int(os.environ.get("ACTIVITY_RANKING_LIMIT", DEFAULT_RANKING_LIMIT))
    timezone = os.environ.get("ACTIVITY_TIMEZONE", DEFAULT_TIMEZONE)
    return ActivitySettings(ranking_limit=ranking_limit, timezone=timezone)
