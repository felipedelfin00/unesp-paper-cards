import os

from config.log import getLogger
from services.transform.transform import transformPapersMulti
from services.transform.insert import insertTransformedPapers
from utils.json import loadJSONL

logger = getLogger(__name__, "pipeline.log")


def run():
    #   Transforming step: reads the extracted raw papers, normalizes the data
    #   and inserts it into the database. Removes the raw papers file after successful insertion.

    papers = loadJSONL("../data/raw.jsonl")
    if not papers:
        logger.warning("No paper to transform.")
        return

    transformed = transformPapersMulti(papers)
    insertTransformedPapers(transformed)

    os.remove("../data/raw.jsonl")
