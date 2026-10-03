from dataclasses import dataclass


@dataclass(frozen=True)
class GroupStatMention:
    user_id: int
    username: str
    full_name: str


@dataclass(frozen=True)
class GroupStatLine:
    """One "label: [mention] value" line of /stats_grupo, kept structured so the
    Telegram layer decides how to render the mention."""

    label: str
    value: str
    mention: GroupStatMention | None = None
