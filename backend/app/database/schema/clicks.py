from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createClicksTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS clicks (
            paperID TEXT NOT NULL,
            clientID TEXT NOT NULL,
            createdAt TEXT NOT NULL,
            FOREIGN KEY(paperID) REFERENCES papers(id) ON DELETE CASCADE
        );
    """)


def createClicksIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_clicks ON clicks(paperID, clientID);
    """)


def createClicks(cursor):
    logger.info("Creating clicks table and indexes.")
    createClicksTable(cursor)
    createClicksIndexes(cursor)
    logger.info("Clicks table and indexes created sucessfully.")
