from dataclasses import dataclass


@dataclass(frozen=True)
class UserPoints:
    user_id: int
    username: str
    full_name: str
    points: int
