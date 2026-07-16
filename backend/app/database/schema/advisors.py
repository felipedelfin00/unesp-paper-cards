from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createAdvisorsTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS advisors (
            paperID TEXT NOT NULL,
            advisor TEXT NOT NULL,
            contact TEXT,
            verified TEXT NOT NULL DEFAULT 'no',
            FOREIGN KEY(paperID) REFERENCES papers(id) ON DELETE CASCADE,
            UNIQUE(paperID, advisor)
        );
    """)


def createAdvisorsIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_advisor ON advisors(advisor);
        CREATE INDEX IF NOT EXISTS idx_verified ON advisors(verified);
    """)


def createAdvisors(cursor):
    logger.info("Creating advisors table and indexes.")
    createAdvisorsTable(cursor)
    createAdvisorsIndexes(cursor)
    logger.info("Advisors table and indexes created sucessfully.")
