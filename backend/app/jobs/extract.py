import requests

from config.log import getLogger
from services.extract.extract import searchNewIDs, fetchPapersMulti, saveRawPapers

logger = getLogger(__name__, "pipeline.log")


def run(limit):
    #   Extracting step: search for new paper IDs  within the configured campus and
    #   downloads their metadata, saving the raw data to disk for the next step.

    session = requests.Session()

    campuses = [
        "Universidade Estadual Paulista (UNESP), Instituto de Biociências, Rio Claro",
        "Universidade Estadual Paulista (UNESP), Instituto de Geociências e Ciências Exatas, Rio Claro",
    ]

    uuids = searchNewIDs(campuses, limit, session)
    if not uuids:
        logger.warning("No new ID found.")
        return

    papers = fetchPapersMulti(uuids, session)
    saveRawPapers(papers)
