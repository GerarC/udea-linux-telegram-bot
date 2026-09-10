import re

# Trigger words for the news-reply feature. Stems are grouped by family and
# expanded with common diminutive/plural suffixes instead of listing every
# variant on its own line.
# NOTE: triggers stay in Spanish on purpose — they match what users actually
# type in the chat.

# Generic suffixes: plural, diminutive, augmentative
_S = r"(?:s|ito|ita|itos|itas|azo|aza|azos|azas)?"

# Multi-word phrases first (they need their own handling, can't use _S)
_PHRASES = [
    r"culo\s+de\s+atr[aá]s",
    r"agujero\s+(?:del\s+culo|anal)",
    r"miembro\s+viril",
    r"verga\s+(?:gorda|grande)",
    r"noticias?(?:\s+de)?\s+(?:tech|tecnolog[íi]a)",
]

_SINGLE_STEMS = {
    # --- tech ---
    "tecnolog[íi]a|inteligencia\s+artificial|machine\s+learning|devops|"
    "kubernetes|ciberseguridad|linux",
    # --- butt ---
    "cul[oa]|culet[ae]|culead[oa]|culear|cule[oa]",
    "nalg[ao]|nalgot[ao]|nalg[oa]n|pompis|pompon[ae]|gl[uú]te[oa]|traser[oa]|"
    "cadera|cachet[ei]|asiento",
    "an[oa]|ojet[ea]|rect[oa]",  # ojo: alto riesgo de falso positivo
    # --- penis ---
    "pene|pito|pija|verga|polla|pollita|rabo|carajo|falo|pichul[oa]",
    # --- vagina ---
    "vagina|vulva|coño|chocho|panocha|cajeta|raj[ao]|hueco|concha|tot[oa]|cuca",
}

TRIGGER_PATTERN = re.compile(
    r"\b(?:" + r"|".join([*_PHRASES, *_SINGLE_STEMS]) + r")\b",
    re.IGNORECASE | re.UNICODE,
)

COOLDOWN_SECONDS = 180  # minimum time between replies in the same chat
RECENT_MEMORY = 40     # how many links to remember per chat to avoid repeats