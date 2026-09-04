# Point thresholds -> level label, evaluated from highest to lowest.
# NOTE: labels stay in Spanish on purpose - they're user-facing copy for the group.
LEVEL_THRESHOLDS: list[tuple[int, str]] = [
    (10000, "Entidad cósmica del autismo, trasciende el plano físico"),
    (5000, "El algoritmo de YouTube le tiene miedo"),
    (2500, "Wikipedia andante con opiniones no solicitadas"),
    (1000, "Su personalidad completa se basa en un solo tópico"),
    (500, "Corrige a la familia en el chat de WhatsApp"),
    (250, "Se sabe el lore completo de algo que a nadie le importa"),
    (100, "Es administrador de un servidor de discord"),
    (50, "Tiene una opinión muy fuerte sobre el orden de las carpetas"),
    (25, "Explica el meme antes de que se lo pidan"),

    (1, "Neurotípico sospechoso"),
    (0, "Increiblemente, una persona normal"),
]

DEFAULT_RANKING_LIMIT = 10
