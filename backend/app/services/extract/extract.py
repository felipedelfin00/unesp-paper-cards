import json
import os
import requests
import time

from config.log import getLogger
from database.connection import getConnection

BASE_URL = "https://repositorio.unesp.br/server/api"
logger = getLogger(__name__, "pipeline.log")


def getExtractedIDs():
    #   Returns the set of IDs of papers alredy saved in the database.

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM papers")
    ids = {row[0] for row in cursor.fetchall()}

    conn.commit()
    conn.close()

    if not ids:
        logger.warning("No ID found in the database.")
        return {}

    logger.info(f"{len(ids)} IDs found in the database.")
    return ids


def searchNewIDs(campuses, limit, session):
    #   Searches the UNESP API for new paper IDs that have not yet been extracted,
    #   filtering by campus. For each campus, it iterates through the result pages
    #   until no objects remain or the limit is reached.

    extractedIDs = getExtractedIDs()
    extraction = set()

    logger.info(f"Search limit: {limit}.")
    for campus in campuses:
        page = 0
        count = 0

        logger.info(f'Searching for IDs in "{campus}" campus.')
        while True:
            url = (
                f"{BASE_URL}/discover/search/objects"
                f"?f.campus={campus},equals"
                "&size=100"
                f"&page={page}"
                "&sort=dc.date.issued,desc"
            )

            #   Attempts the request 3 times before giving up.
            for attempt in range(3):
                try:
                    r = session.get(url, timeout=15)
                    r.raise_for_status()
                    data = r.json()

                    break

                except requests.RequestException:
                    logger.error(
                        f"Unable to extract an ID. [Attempt {attempt + 1} / 3]",
                        exc_info=True,
                    )

                    if attempt == 2:
                        raise

                    time.sleep(5)

            objects = (
                data.get("_embedded", {})
                .get("searchResult", {})
                .get("_embedded", {})
                .get("objects", [])
            )

            if not objects:
                logger.info("End of pagination.")
                break

            for o in objects:
                uuid = o.get("_embedded", {}).get("indexableObject", {}).get("uuid")

                #   Ignores IDs that are already in the database or have already been extracted.
                if (uuid in extractedIDs) or (uuid in extraction):
                    continue

                extraction.add(uuid)
                count += 1

                if (limit is not None) and (count >= limit):
                    break

            if (limit is not None) and (count >= limit):
                break

            page += 1

    logger.info("Search for new IDs completed.")
    return list(extraction)


def fetchPaper(uuid, session):
    #   Retrieves the full paper metadata using an ID.

    url = f"{BASE_URL}/core/items/{uuid}"

    for attempt in range(3):
        try:
            r = session.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()

            return {"uuid": data.get("uuid"), "metadata": data.get("metadata", {})}

        except requests.RequestException:
            logger.error(
                f"Unable to extract metadata from an ID. [Attempt {attempt + 1} / 3]",
                exc_info=True,
            )

            if attempt == 2:
                raise

            time.sleep(5)

    return None


def fetchPapersMulti(uuids, session):
    #   Retrieves metadata for multiple paper, with a brief pause between
    #   requests to avoid overloading the API.

    papers = []
    count = len(uuids)

    for i, uuid in enumerate(uuids, 1):
        logger.info(f"Extracting data. [{i} / {count}]")

        paper = fetchPaper(uuid, session)
        if paper:
            papers.append(paper)

        time.sleep(0.25)

    logger.info("Metadata extraction completed.")
    return papers


def saveRawPapers(papers):
    #   Saves the raw papers to a JSONL file.
    
    os.makedirs(os.path.dirname("../data/raw.jsonl"), exist_ok=True)

    with open("../data/raw.jsonl", "a", encoding="utf-8") as f:
        for paper in papers:
            f.write(json.dumps(paper, ensure_ascii=False) + "\n")

    logger.info("Extracted data sucessfully saved.")
