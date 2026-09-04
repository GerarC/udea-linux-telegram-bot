import re

# Words/phrases that trigger the feature. re.VERBOSE ignores whitespace in the
# pattern, so literal spaces are written as \s+.
# NOTE: the trigger words themselves stay in Spanish on purpose — they match
# what Spanish-speaking users actually type in the chat.
TRIGGER_PATTERN = re.compile(r"""
    \b(
    # --- Original tech terms ---
    noticias?(\s+de)?\s+(tech|tecnolog[íi]a)
    | tecnolog[íi]a
    | inteligencia\s+artificial
    | machine\s+learning
    | devops
    | kubernetes
    | ciberseguridad
    | linux

    # --- Culo y variantes ---
    | cul[oa]s?
    | culit[oa]s?
    | culaz[oa]s?
    | culon[ae]s?
    | culete?s?
    | culete?s?
    | culear
    | culeado[as]?
    | culeand[oa]
    | culeo
    | culeada

    # --- Prepucio y variantes ---
    | prepuci[oa]s?
    | prepucios?
    | prepucito?s?
    | foreskin
    | capuch[oa]s?          # slang común

    # --- Ano y variantes ---
    | anos?
    | anitos?
    | anill[oa]s?
    | ojete?s?
    | ojitos?
    | rect[oa]s?
    | culo\s+de\s+atr[aá]s
    | agujero\s+del\s+culo
    | agujero\s+anal

    # --- Nalgas y variantes ---
    | nalg[ao]s?
    | nalguit[ao]s?
    | nalgot[ao]s?
    | nalgon[ao]s?
    | pompis?
    | pompon[ae]s?
    | gl[uú]te[oa]s?
    | trasero?s?
    | traseros?
    | caderas?
    | cachetes?
    | cachetitos?
    | asientos?             # a veces se usa eufemísticamente

    # --- Pene y variantes ---
    | penes?
    | pene?s?
    | pito?s?
    | pija?s?
    | verg[ao]s?
    | verg[uü]ita?s?
    | verg[oó]n
    | polla?s?
    | pollitas?
    | bicho?s?
    | rabo?s?
    | carajo?s?
    | miembro\s+viril
    | falo?s?
    | pija
    | pene?cito?s?
    | pija?cita?s?
    | verga\s+gorda
    | verga\s+grande

    # --- Vagina y variantes ---
    | vaginas?
    | vagi?nas?
    | co[ñn]os?
    | co[ñn]itos?
    | chochos?
    | chochit[oa]s?
    | panochas?
    | panochitas?
    | cajetas?
    | cajetitas?
    | vulvas?
    | vulvitas?
    | raja?s?
    | rajitas?
    | hueco?s?
    | huecitos?
    | concha?s?
    | conchitas?
    | papa?s?               # algunos países
    | papita?s?
    | totos?
    | totitos?
    | cuca?s?
    | cucitas?
    | panocha
    | chimb[oa]s?
    | panochita
    )\b
""", re.IGNORECASE | re.VERBOSE | re.UNICODE)
COOLDOWN_SECONDS = 60  # minimum time between replies in the same chat
RECENT_MEMORY = 20  # how many links to remember per chat to avoid repeats
