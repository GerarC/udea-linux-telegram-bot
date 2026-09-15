from dataclasses import dataclass


@dataclass(frozen=True)
class ConfessionTitle:
    emoji: str
    title: str
    footer: str
