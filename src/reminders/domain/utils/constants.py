import re

TIMEZONE = "America/Bogota"

# NOTE: user-facing syntax is Spanish ("<mensaje> en <N> <unidad>") since the bot
# serves a Spanish-speaking group. Accepts minutes, hours or days as the unit.
REMINDER_PATTERN = re.compile(
    r"^(?P<message>.+?)\s+en\s+(?P<amount>\d+)\s*(?P<unit>min(?:uto)?s?|h(?:ora)?s?|d(?:í|i)as?)$",
    re.IGNORECASE,
)

MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR

MIN_REMINDER_MINUTES = 1
MAX_REMINDER_MINUTES = 7 * MINUTES_PER_DAY  # 1 semana

USAGE_EXAMPLE = (
    "Usa: /recordar <mensaje> en <cantidad> <minutos|horas|días>. "
    "Ej: /recordar sacar la basura en 30 min, /recordar reunión en 2 horas."
)
