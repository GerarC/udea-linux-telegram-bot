from dataclasses import dataclass


@dataclass(frozen=True)
class Poll:
    question: str
    options: list[str]
