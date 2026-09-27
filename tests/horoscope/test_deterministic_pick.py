from horoscope.domain.utils.deterministic_pick import (
    deterministic_choice,
    deterministic_index,
    deterministic_permutation,
)


def test_deterministic_index_is_stable_for_the_same_seed():
    assert deterministic_index("seed", 100) == deterministic_index("seed", 100)


def test_deterministic_index_stays_within_bounds():
    for _ in range(20):
        assert 0 <= deterministic_index("seed", 7) < 7


def test_deterministic_index_of_a_zero_size_is_zero():
    assert deterministic_index("seed", 0) == 0


def test_deterministic_choice_is_stable_and_picks_an_element_from_the_options():
    options = ["a", "b", "c", "d"]

    assert deterministic_choice("seed", options) in options
    assert deterministic_choice("seed", options) == deterministic_choice("seed", options)


def test_deterministic_permutation_is_a_permutation_of_the_full_range():
    result = deterministic_permutation("seed", 10)

    assert sorted(result) == list(range(10))


def test_deterministic_permutation_is_stable_for_the_same_seed():
    assert deterministic_permutation("seed", 10) == deterministic_permutation("seed", 10)
