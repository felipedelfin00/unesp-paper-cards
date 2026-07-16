from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createKeywordsTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS keywords (
            paperID TEXT NOT NULL,
            keyword TEXT NOT NULL,
            keywordNorm TEXT NOT NULL,
            keywordLanguage TEXT,
            FOREIGN KEY(paperID) REFERENCES papers(id) ON DELETE CASCADE,
            UNIQUE(paperID, keyword)
        );
    """)


def createKeywordsIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_keyword ON keywords(keywordNorm);
    """)


def createKeywords(cursor):
    logger.info("Creating keywords table and indexes.")
    createKeywordsTable(cursor)
    createKeywordsIndexes(cursor)
    logger.info("Keywords table and indexes created sucessfully.")
