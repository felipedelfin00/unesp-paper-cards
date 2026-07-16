from datetime import datetime, timezone, timedelta

from database.connection import getConnection


def addClick(pid, clientID):
    #   Registers a click on a paper, with deduplication.
    conn = getConnection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc)
    window = now - timedelta(hours=1)

    #   Chceks if a click with the same clientID already exists from the last hour.
    cursor.execute(
        "SELECT 1 FROM clicks WHERE paperID = ? AND clientID = ? AND createdAt >= ? LIMIT 1",
        (pid, clientID, window.isoformat()),
    )

    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute(
        "INSERT INTO clicks (paperID, clientID, createdAt) VALUES (?, ?, ?)",
        (pid, clientID, now.isoformat()),
    )

    cursor.execute(
        "UPDATE papers SET clickCount = COALESCE(clickCount, 0) + 1 WHERE id = ?",
        (pid,),
    )

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    return updated > 0
