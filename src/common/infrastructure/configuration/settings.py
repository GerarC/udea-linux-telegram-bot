import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    log_level: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


def load_settings() -> Settings:
    required = {
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN"),
        "DB_HOST": os.environ.get("DB_HOST"),
        "DB_NAME": os.environ.get("DB_NAME"),
        "DB_USER": os.environ.get("DB_USER"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise SystemExit(f"Missing environment variable(s): {', '.join(missing)}")

    return Settings(
        telegram_bot_token=required["TELEGRAM_BOT_TOKEN"],
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
        db_host=required["DB_HOST"],
        db_port=int(os.environ.get("DB_PORT", 5432)),
        db_name=required["DB_NAME"],
        db_user=required["DB_USER"],
        db_password=required["DB_PASSWORD"],
    )
