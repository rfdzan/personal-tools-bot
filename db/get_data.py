import sqlite3
from os import chdir
from pathlib import Path

chdir(Path(__file__).parent.parent)


def db_connect():
    return sqlite3.connect("db/sqlite_db/tmdb.db")


def query_db(search: str):
    search = search.replace(" ", "%")
    conn = db_connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tmdb WHERE title LIKE ?", (f"%{search}%",))
        for id, title in cursor:
            yield id, title
