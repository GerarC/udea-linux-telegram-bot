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
