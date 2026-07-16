from config.log import getLogger

logger = getLogger(__name__, "database.log")


def createPapersTable(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            titleNorm TEXT NOT NULL,
            titleLanguage TEXT,
            titleAlt TEXT,
            titleAltNorm TEXT,
            titleAltLanguage TEXT,
            abstract TEXT,
            summary TEXT,
            socialRelevance TEXT,
            knowledgeArea TEXT,
            knowledgeAreaNorm TEXT,
            paperType TEXT NOT NULL,
            yearIssued INTEGER NOT NULL,
            link TEXT NOT NULL,
            language TEXT NOT NULL DEFAULT 'pt',
            createdAt TEXT NOT NULL DEFAULT current_timestamp,
            updatedAt TEXT NOT NULL DEFAULT current_timestamp,
            version INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'inactive',
            theme TEXT NOT NULL DEFAULT 'default',
            clickCount INTEGER NOT NULL DEFAULT 0  
        );
    """)


def createPapersIndexes(cursor):
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_title ON papers(titleNorm);
        CREATE INDEX IF NOT EXISTS idx_titlealt ON papers(titleAltNorm);
        CREATE INDEX IF NOT EXISTS idx_knowledge ON papers(knowledgeAreaNorm);
        CREATE INDEX IF NOT EXISTS idx_type ON papers(paperType);
        CREATE INDEX IF NOT EXISTS idx_year ON papers(yearIssued);
        CREATE INDEX IF NOT EXISTS idx_language ON papers(language);
        CREATE INDEX IF NOT EXISTS idx_created ON papers(createdAt);
        CREATE INDEX IF NOT EXISTS idx_updated ON papers(updatedAt);
        CREATE INDEX IF NOT EXISTS idx_version ON papers(version);
        CREATE INDEX IF NOT EXISTS idx_status ON papers(status);
        CREATE INDEX IF NOT EXISTS idx_theme ON papers(theme);
        CREATE INDEX IF NOT EXISTS idx_click ON papers(clickCount);
    """)


def createPapers(cursor):
    logger.info("Creating papers table and indexes.")
    createPapersTable(cursor)
    createPapersIndexes(cursor)
    logger.info("Papers table and indexes created sucessfully.")
