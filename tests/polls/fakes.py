from polls.domain.spi.poll_repository_port import PollRepositoryPort


class FakePollRepository(PollRepositoryPort):
    def __init__(self) -> None:
        self.saved: list[tuple[int, int, str, str]] = []
        self.poll_counts: dict[tuple[int, int], int] = {}
        self.chat_poll_counts: dict[int, int] = {}

    async def save_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None:
        self.saved.append((chat_id, user_id, username, question))
        self.poll_counts[(chat_id, user_id)] = self.poll_counts.get((chat_id, user_id), 0) + 1
        self.chat_poll_counts[chat_id] = self.chat_poll_counts.get(chat_id, 0) + 1

    async def get_poll_count(self, chat_id: int, user_id: int) -> int:
        return self.poll_counts.get((chat_id, user_id), 0)

    async def get_chat_poll_count(self, chat_id: int) -> int:
        return self.chat_poll_counts.get(chat_id, 0)
