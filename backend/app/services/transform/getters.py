def getFirstOrEmpty(values):
    #   Returns the first element of the list, or a empty string if the list is empty.
    
    return values[0] if values else ""


def getValues(field, data):
    #   Extract values from a metadata field, ignoring empty entries
    
    return [v.get("value") for v in data.get(field, []) if v.get("value")]


def getValuesAndLanguage(field, data):
    #   Extract value and language from a metadata field, returning a list of dicts,
    #   ignoring empty entries.
    
    result = []

    for v in data.get(field, []):
        if v.get("value"):
            result.append({"value": v.get("value"), "language": v.get("language", "")})

    return result


def getTitles(data):
    #   Gets the papers's main and alternative titles.
    #   If the main title is not in portuguese but the alternative one is, it swaps them.
    
    title = getValuesAndLanguage("dc.title", data)
    alternative = getValuesAndLanguage("dc.title.alternative", data)

    title = title[0] if title else {}
    alternative = alternative[0] if alternative else {}

    if title.get("language", "") != "pt" and alternative.get("language", "") == "pt":
        title, alternative = alternative, title

    return {"title": title, "alternative": alternative}
