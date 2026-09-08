# NOTE: timezone the group operates in, used to compute "today" so the daily
# reading flips at local midnight instead of UTC midnight.
TIMEZONE = "America/Bogota"

# NOTE: Spanish sign names - user-facing copy, also used as the values accepted
# by the /horoscopo command argument.
VALID_SIGNS = [
    "aries",
    "tauro",
    "geminis",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "escorpio",
    "sagitario",
    "capricornio",
    "acuario",
    "piscis",
]

LUCKY_COLORS = [
    "verde terminal",
    "azul pantalla de la muerte",
    "negro consola",
    "amarillo warning",
    "rojo error 500",
    "morado dark mode",
    "gris kernel panic",
    "naranja soldadura fría",
    "blanco whitespace",
    "cian syntax highlight",
]

MOODS = [
    "en modo debug existencial",
    "con hambre de uptime",
    "paranoico por un CVE",
    "eufórico porque compiló a la primera",
    "resignado ante un merge conflict",
    "en negación sobre sus backups",
    "con el ego de un sudoer",
    "nostálgico de cuando internet andaba con módem",
    "ansioso esperando el CI",
    "zen, como root en producción sin miedo",
]

LUCKY_TIMES = [
    "3:14 AM (hora de deploys arriesgados)",
    "9:00 AM (daily standup)",
    "12:00 PM (cronjob de mediodía)",
    "4:04 PM (404 de la tarde)",
    "6:66 PM (hora inexistente, como tu documentación)",
    "11:59 PM (justo antes del deadline)",
    "1:23 AM (debugging nocturno)",
    "8:08 AM (backup automático)",
    "2:22 PM (siesta post-almuerzo)",
    "10:10 PM (hora de romper el ambiente de staging)",
]

LUCKY_NUMBER_MIN = 0
LUCKY_NUMBER_MAX = 127
