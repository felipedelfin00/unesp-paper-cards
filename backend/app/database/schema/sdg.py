from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createSDGTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS sdg (
            paperID TEXT NOT NULL,
            sdg INTEGER NOT NULL,
            reason TEXT,
            FOREIGN KEY(paperID) REFERENCES papers(id) ON DELETE CASCADE,
            UNIQUE(paperID, sdg)
        );
    """)


def createSDGIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_sdg ON sdg(sdg);
    """)


def createSDG(cursor):
    logger.info("Creating SDG table and indexes.")
    createSDGTable(cursor)
    createSDGIndexes(cursor)
    logger.info("SDG table and indexes created sucessfully.")
