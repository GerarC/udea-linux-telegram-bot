import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    log_level: str


def load_settings() -> Settings:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN environment variable")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    return Settings(telegram_bot_token=token, log_level=log_level)
