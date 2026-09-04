from dataclasses import dataclass


@dataclass(frozen=True)
class UserInfoSection:
    title: str
    lines: list[str]
