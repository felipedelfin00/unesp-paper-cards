from database.connection import getConnection


def getAdvisors(cursor, pid):
    #   Returns the advisors list.
    
    cursor.execute("SELECT advisor, contact FROM advisors WHERE paperID = ?", (pid,))
    return [{"advisor": row[0], "contact": row[1]} for row in cursor.fetchall()]


def getAuthors(cursor, pid):
    #   Returns the authors list.
    
    cursor.execute("SELECT author, contact FROM authors WHERE paperID = ?", (pid,))
    return [{"author": row[0], "contact": row[1]} for row in cursor.fetchall()]


def getCampuses(cursor, pid):
    #   Returns the campuses list.
    
    cursor.execute("SELECT campus FROM campuses WHERE paperID = ?", (pid,))
    return [row[0] for row in cursor.fetchall()]


def getKeywords(cursor, pid):
    #   Returns the keywords list, prioritizing the ones in portuguese.
    
    cursor.execute(
        """
        SELECT keyword FROM keywords WHERE paperID = ?
        ORDER BY CASE keywordLanguage
                WHEN 'pt' THEN 1
                WHEN 'en' THEN 2
                ELSE 3
            END,
            keyword ASC
        """,
        (pid,),
    )
    return [row[0] for row in cursor.fetchall()]


def getSDG(cursor, pid):
    #   Returns the SDG list.
    
    cursor.execute(
        "SELECT sdg, reason FROM sdg WHERE paperID = ? ORDER BY sdg ASC", (pid,)
    )
    return [{"number": row[0], "reason": row[1]} for row in cursor.fetchall()]


def getCard(pid):
    #   Builds the full card for exibition.
    
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            summary,
            socialRelevance,
            knowledgeArea,
            paperType,
            yearIssued,
            link,
            language,
            theme
        FROM papers
        WHERE id = ?
        """,
        (pid,),
    )

    row = cursor.fetchone()
    if row is None:
        return None

    columns = [column[0] for column in cursor.description]
    card = dict(zip(columns, row))

    card["advisors"] = getAdvisors(cursor, pid)
    card["authors"] = getAuthors(cursor, pid)
    card["campuses"] = getCampuses(cursor, pid)
    card["keywords"] = getKeywords(cursor, pid)
    card["sdg"] = getSDG(cursor, pid)

    return card
