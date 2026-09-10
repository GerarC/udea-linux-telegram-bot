from dataclasses import dataclass


@dataclass
class ParsedReminder:
    message: str
    minutes: int
