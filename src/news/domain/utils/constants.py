import re

# Trigger words for the news-reply feature. Each stem gets a generic suffix
# group appended, so plural/diminutive/augmentative variants (culito, culazo,
# pijitas...) are covered without listing them individually.
# NOTE: triggers stay in Spanish on purpose — they match what users actually
# type in the chat.

# Common suffixes expanded per stem: plural / diminutive / augmentative
_SUF = r"(?:s|ito|ita|itos|itas|azo|aza|azos|azas|ón|ona|otes|otas)?"

_PHRASES = [
    r"culo\s+de\s+atr[aá]s",
    r"agujero\s+(?:del\s+culo|anal)",
    r"miembro\s+viril",
    r"verga\s+(?:gorda|grande)",
    r"noticias?(?:\s+de)?\s+(?:tech|tecnolog[íi]a)",
]

_STEMS = [
    # --- tech ---
    r"tecnolog[íi]a",
    r"inteligencia\s+artificial",
    r"machine\s+learning",
    r"devops",
    r"kubernetes",
    r"ciberseguridad",
    r"linux",
    # --- butt ---
    r"cul[oa]", r"culet[ae]", r"culead[oa]", r"culear",
    r"nalg(?:[ao]|ot[ao]|ón|ona)", r"pompis?", 
    r"gl[uú]te[oa]", r"traser[oa]", r"cadera", r"cachet[ei]",
    # --- risky stems (revisar falsos positivos) ---
    r"an[oa]", r"ojet[ea]", r"rect[oa]",
    # --- penis ---
    r"pene", r"pito", r"pija", r"verga", r"polla", r"pollita",
    r"rabo", r"falo", r"pichul[oa]",
    # --- vagina ---
    r"vagina", r"vulva", r"coño", r"chocho", r"panocha",
    r"cajeta", r"raj[ao]", r"hueco", r"concha", r"tot[oa]", r"cuca",
]

TRIGGER_PATTERN = re.compile(
    r"\b(?:" + r"|".join([*_PHRASES, *[s + _SUF for s in _STEMS]]) + r")\b",
    re.IGNORECASE | re.UNICODE,
)

COOLDOWN_SECONDS = 180  # minimum time between replies in the same chat
RECENT_MEMORY = 40     # how many links to remember per chat to avoid repeats