from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createAuthorsTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            paperID TEXT NOT NULL,
            author TEXT NOT NULL,
            contact TEXT,
            verified TEXT NOT NULL DEFAULT 'no',
            FOREIGN KEY(paperID) REFERENCES papers(id) ON DELETE CASCADE,
            UNIQUE(paperID, author)
        );
    """)


def createAuthorsIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_author ON authors(author);
        CREATE INDEX IF NOT EXISTS idx_verified ON authors(verified);
    """)


def createAuthors(cursor):
    logger.info("Creating authors table and indexes.")
    createAuthorsTable(cursor)
    createAuthorsIndexes(cursor)
    logger.info("Authors table and indexes created sucessfully.")
