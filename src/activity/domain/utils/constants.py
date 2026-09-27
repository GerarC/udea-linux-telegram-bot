DEFAULT_RANKING_LIMIT = 5

# NOTE: how many months (including the current one) /actividad_grupo charts.
MONTHLY_HISTORY_WINDOW = 6

# NOTE: Spanish month abbreviations - user-facing copy. Index matches date.month - 1.
MONTH_ABBREVIATIONS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

# NOTE: timezone the group operates in, used to compute month boundaries and the
# peak activity hour/weekday in local time instead of UTC.
DEFAULT_TIMEZONE = "America/Bogota"

# NOTE: Spanish labels - user-facing copy. Index matches datetime.weekday() (0=Monday).
WEEKDAY_LABELS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
