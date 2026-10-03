from dataclasses import dataclass


@dataclass(frozen=True)
class BanterStat:
    user_id: int
    username: str
    full_name: str
    insults_received: int
    compliments_received: int
