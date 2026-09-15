import unicodedata


def strip_accents(text: str) -> str:
    """Removes diacritics (e.g. 'géminis' -> 'geminis') so input matches regardless of accents."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))
