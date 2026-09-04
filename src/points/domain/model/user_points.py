from dataclasses import dataclass


@dataclass(frozen=True)
class UserPoints:
    user_id: int
    username: str
    points: int
