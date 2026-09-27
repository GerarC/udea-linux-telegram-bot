from dataclasses import dataclass

from banter.domain.model.banter_stat import BanterStat


@dataclass(frozen=True)
class TopBanterStats:
    most_insulted: BanterStat | None
    most_complimented: BanterStat | None
