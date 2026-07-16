from config.log import getLogger
from database.connection import getConnection

logger = getLogger(__name__, "pipeline.log")


def insertTransformedPapers(papers):
    #   Inserts a list of transformed papers into the database,
    #   including related tables.

    conn = getConnection()
    cursor = conn.cursor()

    for paper in papers:
        pid = paper.get("id")

        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO papers (
                    id,
                    title,
                    titleNorm,
                    titleLanguage,
                    titleAlt,
                    titleAltNorm,
                    titleAltLanguage,
                    abstract,
                    paperType,
                    yearIssued,
                    link,
                    language,
                    createdAt,
                    updatedAt,
                    version,
                    status,
                    theme
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    pid,
                    paper.get("title"),
                    paper.get("titleNorm"),
                    paper.get("titleLanguage", ""),
                    paper.get("titleAlt", ""),
                    paper.get("titleAltNorm", ""),
                    paper.get("titleAltLanguage", ""),
                    paper.get("abstract", ""),
                    paper.get("paperType"),
                    paper.get("yearIssued"),
                    paper.get("link"),
                    paper.get("language"),
                    paper.get("createdAt"),
                    paper.get("updatedAt"),
                    paper.get("version"),
                    paper.get("status"),
                    paper.get("theme"),
                ),
            )

            #   If the paper already exists, skip insertion into the related tables to avoid duplication.
            if cursor.rowcount == 0:
                continue

            for a in paper.get("advisors", []):
                cursor.execute(
                    "INSERT OR IGNORE INTO advisors (paperID, advisor) VALUES (?, ?)",
                    (pid, a),
                )

            for a in paper.get("authors", []):
                cursor.execute(
                    "INSERT OR IGNORE INTO authors (paperID, author) VALUES (?, ?)",
                    (pid, a),
                )

            for c in paper.get("campuses", []):
                cursor.execute(
                    "INSERT OR IGNORE INTO campuses (paperID, campus) VALUES (?, ?)",
                    (pid, c),
                )

            for kw in paper.get("keywords", []):
                if isinstance(kw, dict):
                    value = kw.get("keyword", "")
                    norm = kw.get("keywordNorm", "")
                    language = kw.get("keywordLanguage", "")

                cursor.execute(
                    "INSERT OR IGNORE INTO keywords (paperID, keyword, keywordNorm, keywordLanguage) VALUES (?, ?, ?, ?)",
                    (pid, value, norm, language),
                )

        except Exception:
            #   Logs the error and proceeds to the next paper without interrupting the batch.
            logger.error("Unable to insert data into database.", exc_info=True)

    logger.info("Data successfully inserted into the database.")

    conn.commit()
    conn.close()
