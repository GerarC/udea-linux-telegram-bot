import hashlib
from typing import Sequence, TypeVar

T = TypeVar("T")


def deterministic_index(seed: str, size: int) -> int:
    if size <= 0:
        return 0
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(digest, 16) % size


def deterministic_choice(seed: str, options: Sequence[T]) -> T:
    return options[deterministic_index(seed, len(options))]


def deterministic_permutation(seed: str, size: int) -> list[int]:
    """Shuffles range(size) deterministically for a given seed (e.g. one shuffle per day).

    Fisher-Yates using deterministic_index for each swap, so it stays hash-based like
    the rest of this module instead of pulling in the (non-cryptographic) random module.
    """
    indices = list(range(size))
    for i in range(size - 1, 0, -1):
        j = deterministic_index(f"{seed}|swap{i}", i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    return indices
