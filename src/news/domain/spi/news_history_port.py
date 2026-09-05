from typing import Protocol


class NewsHistoryPort(Protocol):
    """Outbound port: per-chat cooldown and already-sent news items."""

    async def try_fire(self, chat_id: int) -> bool:
        """Atomically checks the cooldown and marks it fired in one step.

        Returns True (and marks fired) only if the cooldown was not active - this
        must be a single atomic operation, not a separate check-then-mark, or two
        concurrent triggers in the same chat can both pass the check and both fire.
        """
        ...

    async def get_recent(self, chat_id: int) -> list[str]: ...

    async def mark_sent(self, chat_id: int, link: str) -> None: ...
