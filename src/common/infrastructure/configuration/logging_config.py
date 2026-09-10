import json
import logging

_STANDARD_ATTRS = set(vars(logging.LogRecord("", 0, "", 0, "", (), None)).keys()) | {"message"}


class JsonFormatter(logging.Formatter):
    """Formats log records as one JSON object per line, so Grafana/Loki can filter by field."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD_ATTRS:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


# NOTE: these third-party loggers are noisy at INFO (e.g. httpx logs every single
# Telegram polling request) and would drown out our own structured business events -
# silenced regardless of the app's configured level.
_NOISY_THIRD_PARTY_LOGGERS = ("httpx", "httpcore", "apscheduler")


def setup_logging(level: int | str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)

    for logger_name in _NOISY_THIRD_PARTY_LOGGERS:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
