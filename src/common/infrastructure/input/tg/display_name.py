import html

from telegram import User


def mention_html(user_id: int, name: str) -> str:
    """Builds an HTML text-mention that tags a user by id, regardless of whether they
    have a username - unlike a plain "@username" string, Telegram renders this as a
    real tap-to-mention notification even for users with no username set."""
    return f'<a href="tg://user?id={user_id}">{html.escape(name)}</a>'


def display_name(user: User) -> str:
    """HTML text-mention for a live Telegram User: shows @username if set, else their
    full name, but always tags the user via their id."""
    name = f"@{user.username}" if user.username else user.full_name
    return mention_html(user.id, name)


def display_name_from_record(user_id: int, username: str, full_name: str) -> str:
    """HTML text-mention for a user read back from storage: @username if they have one,
    else their stored full name, else a generic placeholder (legacy rows not yet
    refreshed by a new message)."""
    name = f"@{username}" if username else (full_name or "alguien")
    return mention_html(user_id, name)
