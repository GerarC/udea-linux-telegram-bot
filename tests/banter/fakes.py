from banter.domain.model.banter_stat import BanterStat
from banter.domain.spi.banter_phrase_port import BanterPhrasePort
from banter.domain.spi.banter_stats_port import BanterStatsPort
from banter.domain.spi.member_lookup_port import MemberLookupPort


class FakeBanterPhrasePort(BanterPhrasePort):
    def __init__(self, insults=None, compliments=None) -> None:
        self.insults = {chat_id: list(phrases) for chat_id, phrases in (insults or {}).items()}
        self.compliments = {chat_id: list(phrases) for chat_id, phrases in (compliments or {}).items()}
        self.added_insults: list[tuple[int, str]] = []
        self.added_compliments: list[tuple[int, str]] = []

    async def get_random_insult(self, chat_id: int) -> str:
        phrases = self.insults.get(chat_id) or []
        return phrases[0] if phrases else ""

    async def get_random_compliment(self, chat_id: int) -> str:
        phrases = self.compliments.get(chat_id) or []
        return phrases[0] if phrases else ""

    async def add_insult(self, chat_id: int, phrase: str) -> None:
        self.added_insults.append((chat_id, phrase))
        self.insults.setdefault(chat_id, []).append(phrase)

    async def add_compliment(self, chat_id: int, phrase: str) -> None:
        self.added_compliments.append((chat_id, phrase))
        self.compliments.setdefault(chat_id, []).append(phrase)


class FakeBanterStatsPort(BanterStatsPort):
    def __init__(self) -> None:
        self.stats: dict[tuple[int, int], BanterStat] = {}

    def _bump(self, chat_id: int, user_id: int, username: str, insults: int = 0, compliments: int = 0) -> None:
        key = (chat_id, user_id)
        current = self.stats.get(key)
        base_insults = current.insults_received if current else 0
        base_compliments = current.compliments_received if current else 0
        self.stats[key] = BanterStat(
            user_id=user_id,
            username=username,
            insults_received=base_insults + insults,
            compliments_received=base_compliments + compliments,
        )

    async def record_insult(self, chat_id: int, user_id: int, username: str) -> None:
        self._bump(chat_id, user_id, username, insults=1)

    async def record_compliment(self, chat_id: int, user_id: int, username: str) -> None:
        self._bump(chat_id, user_id, username, compliments=1)

    async def get_stats(self, chat_id: int, user_id: int) -> BanterStat | None:
        return self.stats.get((chat_id, user_id))

    async def get_most_insulted(self, chat_id: int) -> BanterStat | None:
        candidates = [stat for (c, _), stat in self.stats.items() if c == chat_id and stat.insults_received > 0]
        return max(candidates, key=lambda stat: stat.insults_received, default=None)

    async def get_most_complimented(self, chat_id: int) -> BanterStat | None:
        candidates = [stat for (c, _), stat in self.stats.items() if c == chat_id and stat.compliments_received > 0]
        return max(candidates, key=lambda stat: stat.compliments_received, default=None)


class FakeMemberLookupPort(MemberLookupPort):
    def __init__(self, members: dict[tuple[int, str], int] | None = None) -> None:
        self.members = dict(members or {})

    async def find_user_id_by_username(self, chat_id: int, username: str) -> int | None:
        return self.members.get((chat_id, username))
