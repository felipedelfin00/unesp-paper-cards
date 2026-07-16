import re
import unicodedata


def normalizeCampus(campus):
    #   Removes the default UNESP prefix from the campus name.
    if not campus:
        return ""

    return campus.replace("Universidade Estadual Paulista (UNESP),", "").strip()


def normalizeKeywords(keywords):
    #   Normalize a list of keywords.
    #   For each item, it generates an uppercase versiona and a normalized version
    #   (lowercase, without accents or punctuation), used for search and display.

    if not keywords:
        return []

    norm = []

    for kw in keywords:
        value = kw.get("value").strip()

        if not value:
            continue

        #   Combine multiples spaces into one.
        value = re.sub(r"\s+", " ", value)
        norm.append(
            {
                "keyword": value.upper(),
                "keywordNorm": normalizeText(value),
                "keywordLanguage": kw.get("language", ""),
            }
        )

    return norm


def normalizeName(name):
    #   Cleans the name by removing unwanted markers and suffixes, and reverses
    #   the "Surname, First Name" to "First Name Surname".

    if not name:
        return ""

    name = (
        name.replace("[UNESP]", "")
        .replace("(UNESP]", "")
        .replace("[UNESP)", "")
        .replace("{UNESP]", "")
        .replace("[UNESP}", "")
        .replace("(nome civil)", "")
        .replace("(nome social)", "")
        .strip()
    )

    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        return f"{parts[1]} {parts[0]}".strip()

    return name


def normalizeText(text):
    #   Normalizes the text for comparison by removing accents, punctuation and multiple spaces,
    #   and converting it to lowercase.

    if not text:
        return ""

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def normalizeYear(date):
    #   Extracts the year from a date string (first 4 characters)

    if not date:
        return ""

    return (date)[:4]
