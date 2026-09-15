from dataclasses import dataclass
from datetime import datetime


@dataclass
class Confession:
    id: int
    chat_id: int
    user_id: int
    content: str
    created_at: datetime
    is_deleted: bool
