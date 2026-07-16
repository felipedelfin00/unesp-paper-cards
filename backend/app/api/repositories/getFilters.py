from database.connection import getConnection


def getFilters():
    #   Returns the available filter values to populate the inteface.
    
    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT paperType
        FROM papers
        WHERE status = 'enriched'
        ORDER BY paperType
    """)
    paperType = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("""
        SELECT DISTINCT campus
        FROM campuses
        ORDER BY campus
    """)
    campus = [row[0] for row in cursor.fetchall()]
    
    
    cursor.execute("""
        SELECT DISTINCT yearIssued
        FROM papers
        WHERE status = 'enriched'
        ORDER BY yearIssued DESC
    """)
    yearIssued = [row[0] for row in cursor.fetchall()]
    
    language = [
        {
            "value": "por",
            "label": "Português"
        },
        {
            "value": "eng",
            "label": "Inglês"
        },
        {
            "value": "esp",
            "label": "Espanhol"
        }
    ]
    
    conn.close()
        
    return {
        "paperType": paperType,
        "language": language,
        "campus": campus,
        "yearIssued": yearIssued
    }