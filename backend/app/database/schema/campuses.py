from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createCampusesTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS campuses (
            paperID TEXT NOT NULL,
            campus TEXT NOT NULL,
            FOREIGN KEY(paperID) REFERENCES papers(id) ON DELETE CASCADE,
            UNIQUE(paperID, campus)
        );
    """)


def createCampusesIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_campus ON campuses(campus);
    """)


def createCampuses(cursor):
    logger.info("Creating campuses table and indexes.")
    createCampusesTable(cursor)
    createCampusesIndexes(cursor)
    logger.info("Campuses table and indexes created sucessfully.")
