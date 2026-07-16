from datetime import datetime, timezone

from config.log import getLogger
from services.transform.getters import *
from utils.normalize import (
    normalizeCampus,
    normalizeKeywords,
    normalizeName,
    normalizeText,
    normalizeYear,
)

logger = getLogger(__name__, "pipeline.log")


def transformPaper(paper):
    #   Transforms a raw paper register derived from original metadata
    #   into a normalized document, ready to be persisted.
    
    data = paper.get("metadata", {})

    titles = getTitles(data)
    title = titles.get("title").get("value", "")
    titleNorm = normalizeText(title)
    titleLanguage = titles.get("title").get("language", "")
    titleAlt = titles.get("alternative", {}).get("value", "")
    titleAltNorm = normalizeText(titleAlt)
    titleAltLanguage = titles.get("alternative", {}).get("language", "")

    abstract = getFirstOrEmpty(getValues("dc.description.abstract", data))
    paperType = getFirstOrEmpty(getValues("dc.type", data))
    yearIssued = normalizeYear(getFirstOrEmpty(getValues("dc.date.issued", data)))
    link = getFirstOrEmpty(getValues("dc.identifier.uri", data))
    language = getFirstOrEmpty(getValues("dc.language.iso", data))
    now = datetime.now(timezone.utc).isoformat()

    advisors = [
        normalizeName(advisor) for advisor in getValues("dc.contributor.advisor", data)
    ]
    authors = [
        normalizeName(author) for author in getValues("dc.contributor.author", data)
    ]
    campuses = [normalizeCampus(campus) for campus in getValues("unesp.campus", data)]
    keywords = normalizeKeywords(getValuesAndLanguage("dc.subject", data))

    return {
        "id": paper.get("uuid"),
        "title": title,
        "titleNorm": titleNorm,
        "titleLanguage": titleLanguage,
        "titleAlt": titleAlt,
        "titleAltNorm": titleAltNorm,
        "titleAltLanguage": titleAltLanguage,
        "abstract": abstract,
        "paperType": paperType,
        "yearIssued": yearIssued,
        "link": link,
        "language": language,
        "createdAt": now,
        "updatedAt": now,
        "version": 0,
        "status": "transformed",        #   Initial status of the processing pipeline.
        "theme": "default",
        "advisors": advisors,
        "authors": authors,
        "campuses": campuses,
        "keywords": keywords,
    }


def transformPapersMulti(papers):
    #   Applies transformPaper() to a paper list.
    
    return [transformPaper(paper) for paper in papers]
