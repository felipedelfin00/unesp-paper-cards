import sqlite3

DB_PATH = "../data/papers.db"


def getConnection():
    #   Opens a connection to the database.
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn
