from database.connection import getConnection
from utils.normalize import normalizeText


def getCards(
    offset,
    q,
    knowledgeArea,
    paperType,
    yearFrom,
    yearTo,
    language,
    advisor,
    author,
    campus,
    sdg,
    sort,
):
    #   Retriaves page of cards featuring a combination of filters, text search and configurable sorting.
    #   Dinamically constructs the SQL query, adding only the necessary JOINs and conditions.

    conn = getConnection()
    cursor = conn.cursor()

    base = """
        SELECT DISTINCT
            papers.id,
            papers.title,
            papers.summary,
            papers.knowledgeArea,
            papers.paperType,
            papers.language,
            papers.yearIssued,
            papers.theme
        FROM papers
    """

    joins = []
    conditions = ["papers.status = 'enriched'"]
    params = []

    #   === SEARCH ===
    #   Search by title, alternative title or keywords, all compared against the normalized version.
    if q:
        qNorm = normalizeText(q)
        like = f"%{qNorm}%"

        joins.append("LEFT JOIN keywords kw ON kw.paperID = papers.id")
        conditions.append(
            "(papers.titleNorm LIKE ? OR papers.titleAltNorm LIKE ? OR kw.keywordNorm LIKE ?)"
        )
        params.extend([like, like, like])

    #   === FILTERS ===
    if knowledgeArea:
        kaNorm = normalizeText(knowledgeArea)
        like = f"%{kaNorm}%"

        conditions.append("papers.knowledgeAreaNorm LIKE ?")
        params.append(like)

    if paperType:
        conditions.append("papers.paperType = ?")
        params.append(paperType)

    if yearFrom:
        conditions.append("papers.yearIssued >= ?")
        params.append(yearFrom)

    if yearTo:
        conditions.append("papers.yearIssued <= ?")
        params.append(yearTo)

    if language:
        conditions.append("papers.language = ?")
        params.append(language)

    if advisor:
        like = f"%{advisor}%"

        joins.append("LEFT JOIN advisors ad ON ad.paperID = papers.id")
        conditions.append("ad.advisor LIKE ?")
        params.append(like)

    if author:
        like = f"%{author}%"

        joins.append("LEFT JOIN authors au ON au.paperID = papers.id")
        conditions.append("au.author LIKE ?")
        params.append(like)

    if campus:
        joins.append("LEFT JOIN campuses cm ON cm.paperID = papers.id")
        conditions.append("cm.campus = ?")
        params.append(campus)

    if sdg:
        #   SDG arrives as a string "4||10||13".

        sdg = [g.strip() for g in sdg.split("||") if g]
        placeholders = ",".join(["?"] * len(sdg))

        conditions.append(f"""
            (SELECT COUNT(DISTINCT sd.sdg) FROM sdg sd
            WHERE sd.paperID = papers.id AND sd.sdg IN ({placeholders})) = ?
        """)
        params.extend(sdg)
        params.append(len(sdg))

    #   === QUERY ASSEMBLY ===
    query = base

    if joins:
        query += " " + " ".join(set(joins))

    whereClause = ""
    if conditions:
        whereClause = " WHERE " + " AND ".join(conditions)

    query += whereClause

    #   === SORTING ===
    if sort == "visits":
        query += (
            " ORDER BY papers.clickCount DESC, papers.yearIssued DESC, papers.title ASC"
        )
    elif sort == "newest":
        query += " ORDER BY papers.yearIssued DESC, papers.title ASC"
    elif sort == "oldest":
        query += " ORDER BY papers.yearIssued ASC, papers.title ASC"
    else:
        query += " ORDER BY RANDOM()"

    #   === PAGINATION ===
    query += " LIMIT ? OFFSET ?"
    paramsQuery = params + [30, offset]  #   30 = fixed page size.

    #   === COUNT ===
    countQuery = "SELECT COUNT(DISTINCT papers.id) FROM papers"

    if joins:
        countQuery += " " + " ".join(set(joins))

    countQuery += whereClause

    #   === EXECUTION ===
    cursor.execute(query, paramsQuery)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    items = []

    for row in rows:
        card = dict(zip(columns, row))
        items.append(card)

    cursor.execute(countQuery, params)
    total = cursor.fetchone()[0]

    conn.close()

    return {"total": total, "items": items}
