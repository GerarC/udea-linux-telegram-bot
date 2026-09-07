from points.domain.utils.constants import LEVEL_THRESHOLDS


def level_for(points: int) -> str:
    for threshold, label in LEVEL_THRESHOLDS:
        if points >= threshold:
            return label
    return LEVEL_THRESHOLDS[-1][1]
