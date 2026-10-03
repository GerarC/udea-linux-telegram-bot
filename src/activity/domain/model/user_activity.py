from dataclasses import dataclass


@dataclass(frozen=True)
class UserActivity:
    user_id: int
    username: str
    full_name: str
    message_count: int
