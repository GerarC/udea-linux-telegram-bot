from points.domain.utils.constants import LEVEL_THRESHOLDS
from points.domain.utils.leveling import level_for


def test_level_for_zero_points_is_the_lowest_label():
    assert level_for(0) == LEVEL_THRESHOLDS[-1][1]


def test_level_for_negative_points_falls_back_to_lowest_label():
    assert level_for(-100) == LEVEL_THRESHOLDS[-1][1]


def test_level_for_exact_threshold_matches_that_label():
    threshold, label = LEVEL_THRESHOLDS[0]
    assert level_for(threshold) == label


def test_level_for_points_above_top_threshold_matches_top_label():
    threshold, label = LEVEL_THRESHOLDS[0]
    assert level_for(threshold + 1000) == label
