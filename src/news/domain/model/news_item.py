from dataclasses import dataclass


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
    source: str
