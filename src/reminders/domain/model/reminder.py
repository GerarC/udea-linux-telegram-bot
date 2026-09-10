from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reminder:
    id: int
    chat_id: int
    user_id: int
    message: str
    remind_at: datetime
    fired: bool
