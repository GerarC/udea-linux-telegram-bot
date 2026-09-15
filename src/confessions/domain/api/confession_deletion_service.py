from typing import Protocol

from confessions.domain.model.confession import Confession


class ConfessionDeletionService(Protocol):
    """Inbound port for the confessions feature: deleting a confession (admins only).

    Returns None when the requester isn't an admin - the Telegram handler already
    has the context to phrase that as a permission message (see telegram-and-errors.md,
    same pattern as points.grant_points).
    """

    async def delete_confession(
        self, chat_id: int, confession_id: int, requester_is_admin: bool
    ) -> Confession | None: ...
