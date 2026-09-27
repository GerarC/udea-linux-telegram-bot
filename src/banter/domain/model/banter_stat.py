from dataclasses import dataclass


@dataclass(frozen=True)
class BanterStat:
    user_id: int
    username: str
    insults_received: int
    compliments_received: int
