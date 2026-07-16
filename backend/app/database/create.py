from config.log import getLogger
from database.connection import getConnection
from database.schema import advisors, authors, campuses, clicks, keywords, papers, sdg

logger = getLogger(__name__, "database.log")


def createDatabase():
    #   Creates all database tables.
    
    logger.info("Creating database.")

    conn = getConnection()
    cursor = conn.cursor()

    papers.createPapers(cursor)
    advisors.createAdvisors(cursor)
    authors.createAuthors(cursor)
    campuses.createCampuses(cursor)
    clicks.createClicks(cursor)
    keywords.createKeywords(cursor)
    sdg.createSDG(cursor)

    conn.commit()
    conn.close()

    logger.info("Database created sucessfully.")
