import re

def sanitize_text(text: str) -> str:
    replacements = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-", "\u00a0": " ", "\u2022": "-"}
    text = text or ""
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = "".join(c for c in text if c in "\n\r\t" or ord(c) >= 32)
    return re.sub(r"\n{4,}", "\n\n\n", text).strip()

def terms_to_list(terms: str) -> list[str]:
    return [x.strip() for x in terms.split(";") if x.strip()]
