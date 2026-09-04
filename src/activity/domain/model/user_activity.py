from dataclasses import dataclass


@dataclass(frozen=True)
class UserActivity:
    user_id: int
    username: str
    message_count: int
