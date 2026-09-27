from telegram import User


def display_name(user: User) -> str:
    """Formats a live Telegram User: @username, or their full name if they have none."""
    return f"@{user.username}" if user.username else user.full_name


def display_name_from_record(user_id: int, username: str) -> str:
    """Formats a (user_id, username) pair read back from storage, where there's no
    full_name to fall back to - just the raw user_id."""
    return f"@{username}" if username else str(user_id)
